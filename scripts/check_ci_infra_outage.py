#!/usr/bin/env python3
"""
check_ci_infra_outage.py — Lessons-learnt deferred patch (v8.3 Phase 3 friction
item 3, resolved 2026-08-07, Head of Engineering)

Classifies a failed GitHub Actions run/job as "infra-outage" vs "real" by
scanning its logs for known GitHub-side infrastructure-failure signature
strings, and detects the "stuck rerun" state that itself masquerades as a
workflow problem. Does not attempt to auto-retry anything — it only reports
a classification so a human/agent doesn't have to open every job log by hand
before deciding whether a red CI check is worth investigating as code.

Problem this closes (Phase 3, 2026-08-05__release-v8.3): a live GitHub
Actions outage (2026-08-06, ~16:00-21:00 UTC, confirmed via githubstatus.com)
caused repeated spurious failures across PR #1259 and #1260. Distinguishing
these from real test failures required manually opening many individual job
logs. Separately, `gh run rerun` on a run already mid-rerun attempt produced
a misleading "workflow file may be broken" error — itself an outage symptom,
not a real workflow-syntax problem.

Known infra-outage signature strings (extend this list as new outage
patterns are confirmed — do not guess new ones without a githubstatus.com-
confirmed incident to back them):
  - "Failed to resolve action download info. Error: Service Unavailable"
    (action-setup phase failure, before any test code runs)
  - "workflow file may be broken" returned by `gh run rerun` while the
    run object still reports `queued` or `in_progress` (stuck-rerun state)
  - Job status stuck at `queued` for an extended window with no `startedAt`
    timestamp advancing (queue-timeout auto-cancellation pattern)

Usage:
    python3 scripts/check_ci_infra_outage.py --run <run-id>
    python3 scripts/check_ci_infra_outage.py --pr <pr-number>

Requires: `gh` CLI authenticated with repo access. Read-only — never
retries or reruns anything itself; that decision stays with the human/agent
reading the classification.

Exit codes:
    0  — classification produced (see stdout; check the "classification"
         field per run/job, not the process exit code, for infra vs real)
    1  — could not fetch data from `gh` (auth/network/API error)
    2  — invalid arguments
"""

import argparse
import json
import subprocess
import sys

INFRA_SIGNATURES = [
    "Failed to resolve action download info",
    "Error: Service Unavailable",
    "workflow file may be broken",
]

STUCK_RERUN_SIGNATURE = "workflow file may be broken"


def run_gh(args):
    """Run a `gh` CLI command and return (exit_code, stdout, stderr)."""
    try:
        result = subprocess.run(
            ["gh"] + args, capture_output=True, text=True, timeout=60
        )
        return result.returncode, result.stdout, result.stderr
    except FileNotFoundError:
        print("ERROR: `gh` CLI not found on PATH.", file=sys.stderr)
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print(f"ERROR: `gh {' '.join(args)}` timed out after 60s.", file=sys.stderr)
        sys.exit(1)


def get_run_jobs(run_id):
    code, out, err = run_gh(
        ["run", "view", str(run_id), "--json", "jobs,status,conclusion"]
    )
    if code != 0:
        print(f"ERROR fetching run {run_id}: {err}", file=sys.stderr)
        sys.exit(1)
    return json.loads(out)


def get_job_log(job_id):
    # `gh run view --log` dumps the full run log; for a single job,
    # `gh api` against the job logs endpoint is more targeted, but the
    # simple `--log-failed` flag (run-level) is sufficient for this
    # scoped check and avoids extra API surface.
    code, out, err = run_gh(["run", "view", "--job", str(job_id), "--log-failed"])
    if code != 0:
        # A non-zero exit here can itself be an infra symptom (e.g. the
        # API is unavailable) — don't hard-fail the whole classification,
        # record it as inconclusive for this job instead.
        return None
    return out


def classify_job(job):
    name = job.get("name", "<unknown job>")
    conclusion = job.get("conclusion")
    status = job.get("status")

    if conclusion not in ("failure", "cancelled", "timed_out"):
        return {"job": name, "classification": "not_failed", "conclusion": conclusion}

    log = get_job_log(job.get("databaseId") or job.get("id"))
    if log is None:
        return {
            "job": name,
            "classification": "inconclusive",
            "reason": "could not fetch job log",
        }

    matched = [sig for sig in INFRA_SIGNATURES if sig in log]
    if matched:
        return {
            "job": name,
            "classification": "infra_outage",
            "matched_signatures": matched,
        }

    # Queue-timeout pattern: cancelled with no real duration (started ==
    # completed, or startedAt missing) is a proxy for "sat queued, then
    # GitHub's own timeout auto-cancelled it" rather than a real failure.
    if conclusion == "cancelled" and not job.get("startedAt"):
        return {
            "job": name,
            "classification": "infra_outage",
            "reason": "cancelled with no startedAt timestamp — likely queue-timeout auto-cancellation",
        }

    return {"job": name, "classification": "real_failure_candidate"}


def classify_run(run_id):
    data = get_run_jobs(run_id)
    jobs = data.get("jobs", [])
    results = [classify_job(j) for j in jobs]
    any_infra = any(r["classification"] == "infra_outage" for r in results)
    any_real = any(r["classification"] == "real_failure_candidate" for r in results)
    overall = (
        "infra_outage"
        if any_infra and not any_real
        else "mixed_or_real"
        if any_real
        else "inconclusive"
    )
    return {"run_id": run_id, "overall": overall, "jobs": results}


def check_stuck_rerun(run_id):
    """Detect the specific 'rerun on an already-mid-rerun run' failure mode."""
    code, out, err = run_gh(["run", "rerun", str(run_id), "--dry-run"])
    combined = (out or "") + (err or "")
    if STUCK_RERUN_SIGNATURE in combined:
        return True
    return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--run", type=int, help="GitHub Actions run ID to classify")
    group.add_argument(
        "--pr", type=int, help="PR number — classify its most recent run(s)"
    )
    args = parser.parse_args()

    if args.pr:
        code, out, err = run_gh(
            [
                "pr",
                "checks",
                str(args.pr),
                "--json",
                "workflow,link,state",
            ]
        )
        if code != 0:
            print(f"ERROR fetching PR #{args.pr} checks: {err}", file=sys.stderr)
            sys.exit(1)
        checks = json.loads(out)
        print(json.dumps(checks, indent=2))
        print(
            "\nNote: run `--run <run-id>` (parse the run ID from each check's link "
            "above) for a per-job infra-vs-real classification.",
            file=sys.stderr,
        )
        return

    result = classify_run(args.run)
    if check_stuck_rerun(args.run):
        result["stuck_rerun_detected"] = True
        result["note"] = (
            "`gh run rerun` reports 'workflow file may be broken' while this run "
            "is still queued/in-progress — this is an outage symptom, not a real "
            "workflow-syntax problem. Do not edit the workflow file in response; "
            "wait and retry, or use an empty retrigger commit on a fresh SHA."
        )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
