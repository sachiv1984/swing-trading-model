#!/usr/bin/env python3
"""
Trigger one staging service's Render deploy hook and confirm the deploy it
started belongs to that service.

ST-29 (BLG-OPS-189, EPIC-05, v9.13). staging-deploy.yml used one secret,
RENDER_STAGING_DEPLOY_HOOK, which held the staging *frontend's* hook while
wait_for_staging_deploy_live.py waited on the *backend*, so every run from
2026-09-03 timed out and the backend changed only by manual deploy. Staging
has two services and a hook deploys exactly one, so each service now has its
own secret (HOOK_ENV below) and its own trigger + wait step.

A mis-pasted hook fails loudly: the deploy ID in the hook's response is
looked up under the expected service (GET /v1/services/{id}/deploys/{deployId});
a 404 there means the hook started a deploy on some other service.

The hook is called with ?ref=<sha> so the service builds the commit that
triggered the workflow, not whatever its Branch setting points at.

check_workflow_wiring() is the static check behind the AC "a test fails if
the workflow calls only one hook or waits on a service it did not deploy"
(tests/test_staging_deploy_both_services.py).

Usage (writes deploy_id=<id> to $GITHUB_OUTPUT when set):
    RENDER_STAGING_BACKEND_DEPLOY_HOOK=... RENDER_PLATFORM_API_KEY=... \\
        python3 scripts/trigger_staging_deploy.py trading-assistant-api-staging <sha>

Exit code: 0 if the hook accepted the trigger and the deploy belongs to the
service; 1 otherwise; 2 on a usage error.
"""
import json
import os
import re
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit, urlunsplit, parse_qsl
from urllib.request import Request, urlopen

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_staging_deploy_drift import RENDER_API_BASE, STAGING_SERVICES, get_render_api_key  # noqa: E402

HOOK_ENV = {
    "trading-assistant-api-staging": "RENDER_STAGING_BACKEND_DEPLOY_HOOK",
    "trading-assistant-staging": "RENDER_STAGING_FRONTEND_DEPLOY_HOOK",
}
RETIRED_HOOK_ENV = "RENDER_STAGING_DEPLOY_HOOK"

WORKFLOW = Path(__file__).resolve().parent.parent / ".github" / "workflows" / "staging-deploy.yml"


def hook_url_with_ref(hook_url: str, sha: str) -> str:
    parts = urlsplit(hook_url)
    query = [(k, v) for k, v in parse_qsl(parts.query) if k != "ref"] + [("ref", sha)]
    return urlunsplit(parts._replace(query=urlencode(query)))


def parse_deploy_id(body: bytes) -> str:
    """Render's hook answers {"deploy": {"id": "dep-..."}}; accept a bare
    {"id": ...} too. Returns "" if no deploy ID is present."""
    try:
        parsed = json.loads(body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return ""
    if isinstance(parsed, dict):
        deploy = parsed.get("deploy") if isinstance(parsed.get("deploy"), dict) else parsed
        deploy_id = deploy.get("id")
        if isinstance(deploy_id, str):
            return deploy_id
    return ""


def deploy_belongs_to_service(service_id: str, deploy_id: str, api_key: str) -> bool:
    """True if Render finds deploy_id under service_id; False on a 404."""
    req = Request(
        f"{RENDER_API_BASE}/services/{service_id}/deploys/{deploy_id}",
        headers={"Authorization": f"Bearer {api_key}", "Accept": "application/json"},
    )
    try:
        with urlopen(req, timeout=15):
            return True
    except HTTPError as e:
        if e.code == 404:
            return False
        raise RuntimeError(f"Render API error looking up {deploy_id} on {service_id}: HTTP {e.code}") from e


def trigger(service_name: str, sha: str, hook_url: str, api_key: str) -> str:
    """Call the hook and verify its deploy. Returns the deploy ID; raises
    RuntimeError with the reason on any failure."""
    service_id = STAGING_SERVICES[service_name]
    try:
        with urlopen(Request(hook_url_with_ref(hook_url, sha), method="POST"), timeout=30) as resp:
            status, body = resp.status, resp.read()
    except HTTPError as e:
        raise RuntimeError(f"{service_name}: deploy hook returned HTTP {e.code}") from e
    except URLError as e:
        raise RuntimeError(f"{service_name}: deploy hook request failed: {e.reason}") from e
    if status not in (200, 201, 202):
        raise RuntimeError(f"{service_name}: deploy hook returned HTTP {status}")
    deploy_id = parse_deploy_id(body)
    if not deploy_id:
        raise RuntimeError(f"{service_name}: deploy hook response has no deploy ID: {body[:200]!r}")
    if not deploy_belongs_to_service(service_id, deploy_id, api_key):
        raise RuntimeError(
            f"{service_name}: deploy {deploy_id} is not a deploy of {service_id}. "
            f"{HOOK_ENV[service_name]} holds another service's hook; copy it again from "
            f"Render dashboard -> {service_name} -> Settings -> Deploy Hook."
        )
    return deploy_id


_TRIGGER_RE = re.compile(r"trigger_staging_deploy\.py\s+(\S+)")
_WAIT_RE = re.compile(r"wait_for_staging_deploy_live\.py\b(.*)")
_SERVICE_ARG_RE = re.compile(r"--service\s+(\S+)")


def check_workflow_wiring(workflow: dict) -> list:
    """Return a list of wiring errors in a parsed staging-deploy.yml (empty
    if it deploys both staging services, each from its own hook secret, and
    waits on exactly the services it deployed)."""
    errors = []
    triggered, waited = [], []
    for job in (workflow.get("jobs") or {}).values():
        for step in job.get("steps") or []:
            run = step.get("run") or ""
            env = step.get("env") or {}
            if RETIRED_HOOK_ENV in run or RETIRED_HOOK_ENV in json.dumps(env):
                errors.append(f"step {step.get('name')!r} still uses the retired {RETIRED_HOOK_ENV}")
            for m in _TRIGGER_RE.finditer(run):
                name = m.group(1).strip("\"'")
                triggered.append(name)
                hook_env = HOOK_ENV.get(name)
                if hook_env is None:
                    errors.append(f"step {step.get('name')!r} triggers unknown service {name!r}")
                elif env.get(hook_env) != f"${{{{ secrets.{hook_env} }}}}":
                    errors.append(f"step {step.get('name')!r} triggers {name} without env {hook_env} from its own secret")
            for m in _WAIT_RE.finditer(run):
                svc = _SERVICE_ARG_RE.search(m.group(1))
                # No --service means the script's default, the backend.
                waited.append(svc.group(1).strip("\"'") if svc else "trading-assistant-api-staging")

    for name in STAGING_SERVICES:
        if name not in triggered:
            errors.append(f"no step calls {name}'s deploy hook ({HOOK_ENV[name]})")
        if name not in waited:
            errors.append(f"no step waits on {name}")
    for name in waited:
        if name not in triggered:
            errors.append(f"a step waits on {name}, which this workflow does not deploy")
    for name in set(triggered):
        if triggered.count(name) > 1:
            errors.append(f"{name}'s deploy hook is called {triggered.count(name)} times")
    return errors


def main() -> int:
    if len(sys.argv) != 3 or sys.argv[1] not in STAGING_SERVICES:
        print(f"Usage: trigger_staging_deploy.py <{'|'.join(STAGING_SERVICES)}> <sha>", file=sys.stderr)
        return 2
    service_name, sha = sys.argv[1], sys.argv[2]
    hook_env = HOOK_ENV[service_name]
    hook_url = os.getenv(hook_env, "")
    if not hook_url:
        print(f"::error::{hook_env} is not set. Copy it from Render dashboard -> {service_name} -> "
              f"Settings -> Deploy Hook into repo Settings -> Secrets and variables -> Actions.")
        return 1
    api_key = get_render_api_key()
    try:
        deploy_id = trigger(service_name, sha, hook_url, api_key)
    except RuntimeError as e:
        print(f"::error::{e}")
        return 1
    print(f"{service_name}: deploy {deploy_id} started for {sha[:10]} on {STAGING_SERVICES[service_name]}.")
    output = os.getenv("GITHUB_OUTPUT")
    if output:
        with open(output, "a") as f:
            f.write(f"deploy_id={deploy_id}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
