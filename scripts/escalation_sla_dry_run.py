#!/usr/bin/env python3
"""
Escalation SLA-breach dry run (ST-43, BLG-GOV-193, EPIC-07, v9.15).

Exercises the escalation SLA-breach path end to end on a SCRATCH COPY of the
state files, never the live `.claude_current_state.json`:

  1. Copies `.claude_current_state.json` and the active cycle's
     `execution_escalations.md` into a temporary directory.
  2. Adds synthetic escalations to the copy: an `Open` one backdated past its
     72h SLA (blocking and non-blocking variants), plus controls (`Deferred`
     and `Resolved`, both past SLA, and an `Open` one inside its SLA).
  3. Evaluates, against the copy, the literal trigger predicate of each rule
     that should fire:
       - shared_standards.md §4 SLA Breach Rule / §16.4 (`BLOCKED_SLA_BREACH`,
         gate `SLA_BREACH`): "open for 72 hours or more without resolution"
       - shared_standards.md §16.4.1 / execution_prompt.md STEP -1.2A advisory:
         `disposition: Open` and `sla_due_utc` earlier than now
       - release_planning_prompt.md STEP -1.6 (`SLA_BREACH_CARRIED`):
         `disposition: Open` and now at or past `sla_due_utc`
     and, for the rule that writes state, applies its writes to the copy
     (the `BLOCKED_SLA_BREACH` notice appended to the copy's escalations file,
     `blocked_sla_breached = true` in the copy's state file).
  4. Runs `.github/workflows/escalation-sla-reminder.yml`'s embedded Python
     verbatim, in the scratch directory, with `gh` replaced by a stub that
     records each call instead of touching GitHub.

The prompt rules are instructions an engine follows, so step 3 evaluates each
rule's written predicate rather than running an engine; step 4 runs the only
mechanical part as written. Results are printed as JSON. The dated record is
`docs/ops/escalation_sla_breach_dry_run_<date>.md`.

Usage: python3 scripts/escalation_sla_dry_run.py [--now ISO-8601] [--keep DIR]
"""
import argparse
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIVE_STATE = ROOT / ".claude_current_state.json"
WORKFLOW = ROOT / ".github" / "workflows" / "escalation-sla-reminder.yml"


def _iso(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse(ts):
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def synthetic_escalations(now):
    raised = now - timedelta(hours=80)
    base = {"cycle": "DRY-RUN", "trigger_type": "Strategy", "owning_authority": "PMO Lead (dry run)"}
    return {
        "ESC-EXEC-DRYRUN-01": {**base, "summary": "Dry run: Open, blocking, 80h old, 8h past SLA",
                               "raised_utc": _iso(raised), "sla_due_utc": _iso(raised + timedelta(hours=72)),
                               "blocks_execution": True, "disposition": "Open"},
        "ESC-EXEC-DRYRUN-02": {**base, "summary": "Dry run: Open, non-blocking, 80h old, 8h past SLA",
                               "raised_utc": _iso(raised), "sla_due_utc": _iso(raised + timedelta(hours=72)),
                               "blocks_execution": False, "disposition": "Open"},
        "ESC-EXEC-DRYRUN-03": {**base, "summary": "Dry run control: Deferred, past SLA",
                               "raised_utc": _iso(raised), "sla_due_utc": _iso(raised + timedelta(hours=72)),
                               "blocks_execution": False, "disposition": "Deferred"},
        "ESC-EXEC-DRYRUN-04": {**base, "summary": "Dry run control: Resolved, past SLA",
                               "raised_utc": _iso(raised), "sla_due_utc": _iso(raised + timedelta(hours=72)),
                               "blocks_execution": True, "disposition": "Resolved"},
        "ESC-EXEC-DRYRUN-05": {**base, "summary": "Dry run control: Open, 10h old, inside SLA",
                               "raised_utc": _iso(now - timedelta(hours=10)),
                               "sla_due_utc": _iso(now + timedelta(hours=62)),
                               "blocks_execution": True, "disposition": "Open"},
    }


UNRESOLVED = {"Open", "Deferred"}  # §4 "without resolution": not Resolved/Accepted Risk/Closed/Withdrawn


def blocked_sla_breach(escs, now):
    """§4 / §16.4: open 72h or more without resolution (any trigger type)."""
    return sorted(e for e, r in escs.items()
                  if r.get("disposition") in UNRESOLVED and r.get("raised_utc")
                  and now - _parse(r["raised_utc"]) >= timedelta(hours=72))


def step_minus_1_2a_advisory(escs, now):
    """execution_prompt.md STEP -1.2A: disposition Open and sla_due_utc earlier than now."""
    return sorted(e for e, r in escs.items()
                  if r.get("disposition") == "Open" and r.get("sla_due_utc") and _parse(r["sla_due_utc"]) < now)


def sla_breach_carried(escs, now):
    """release_planning_prompt.md STEP -1.6: disposition Open and now at or past sla_due_utc."""
    return sorted(e for e, r in escs.items()
                  if r.get("disposition") == "Open" and r.get("sla_due_utc") and now >= _parse(r["sla_due_utc"]))


def workflow_python(text):
    m = re.search(r"python3 - <<'PYEOF'\n(.*?)\n\s*PYEOF", text, re.S)
    if not m:
        raise ValueError("embedded Python not found in escalation-sla-reminder.yml")
    lines = m.group(1).split("\n")
    indent = min(len(l) - len(l.lstrip()) for l in lines if l.strip())
    return "\n".join(l[indent:] for l in lines)


GH_STUB = """#!/usr/bin/env python3
import json, os, sys
with open(os.environ["GH_CALL_LOG"], "a") as f:
    f.write(json.dumps(sys.argv[1:]) + "\\n")
if sys.argv[1:3] == ["issue", "list"]:
    print(os.environ.get("GH_STUB_ISSUES", "[]"))
"""


def run_workflow(scratch, existing_issues="[]", now=None):
    """Run the workflow's Python in `scratch` with a recording gh stub.
    `now` is pinned by shifting datetime.now inside the script."""
    code = workflow_python(WORKFLOW.read_text())
    if now is not None:
        code = ("import datetime as _dt\n"
                f"class _Pinned(_dt.datetime):\n"
                f"    @classmethod\n"
                f"    def now(cls, tz=None):\n"
                f"        return _dt.datetime.fromisoformat({now.isoformat()!r})\n"
                "_dt.datetime = _Pinned\n") + code
    bindir = scratch / "bin"
    bindir.mkdir(exist_ok=True)
    gh = bindir / "gh"
    gh.write_text(GH_STUB)
    gh.chmod(gh.stat().st_mode | stat.S_IEXEC)
    log = scratch / "gh_calls.jsonl"
    log.write_text("")
    env = {**os.environ, "PATH": f"{bindir}{os.pathsep}{os.environ['PATH']}", "REPO": "dry-run/repo",
           "GH_CALL_LOG": str(log), "GH_STUB_ISSUES": existing_issues}
    proc = subprocess.run([sys.executable, "-c", code], cwd=scratch, env=env, capture_output=True, text=True)
    calls = [json.loads(l) for l in log.read_text().splitlines() if l]
    return {"returncode": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr, "gh_calls": calls}


def notice(esc_id, rec, now):
    hours = int((now - _parse(rec["raised_utc"])).total_seconds() // 3600)
    return (f"\n## BLOCKED_SLA_BREACH — {esc_id} (dry run)\n\n"
            f"🛑 HALT — SLA_BREACH\n"
            f"- **Unblock criteria:** {rec['owning_authority']} resolves {esc_id} (open {hours}h, ≥72h)\n"
            f"- **Status:** Pending\n")


def dry_run(now, keep=None):
    live_before = LIVE_STATE.read_bytes()
    scratch = Path(keep) if keep else Path(tempfile.mkdtemp(prefix="st43_sla_dry_run_"))
    scratch.mkdir(parents=True, exist_ok=True)
    try:
        state_path = scratch / ".claude_current_state.json"
        shutil.copyfile(LIVE_STATE, state_path)
        state = json.loads(state_path.read_text())
        live_esc = ROOT / "claude" / "cycles" / state["active_cycle"] / "execution_escalations.md"
        esc_path = scratch / "execution_escalations.md"
        if live_esc.exists():
            shutil.copyfile(live_esc, esc_path)
        else:
            esc_path.write_text("# Execution Escalations\n")

        baseline = dict(state.get("open_escalations") or {})
        result = {"now": _iso(now), "scratch_dir": str(scratch), "baseline": {
            "blocked_sla_breach": blocked_sla_breach(baseline, now),
            "step_minus_1_2a_advisory": step_minus_1_2a_advisory(baseline, now),
            "sla_breach_carried": sla_breach_carried(baseline, now),
            "workflow": run_workflow(scratch, now=now),
        }}

        synth = synthetic_escalations(now)
        state["open_escalations"] = {**baseline, **synth}
        escs = state["open_escalations"]
        breach = blocked_sla_breach(escs, now)
        # Apply §16.4's writes to the copy only.
        with esc_path.open("a") as f:
            for e in breach:
                if e in synth:
                    f.write(notice(e, escs[e], now))
        if breach:
            state["blocked_sla_breached"] = True
        state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n")

        result["synthetic"] = {
            "ids": sorted(synth),
            "blocked_sla_breach": breach,
            "blocked_sla_breached_written": json.loads(state_path.read_text()).get("blocked_sla_breached"),
            "notices_in_scratch_escalations": re.findall(r"^## BLOCKED_SLA_BREACH — (\S+)", esc_path.read_text(), re.M),
            "step_minus_1_2a_advisory": step_minus_1_2a_advisory(escs, now),
            "sla_breach_carried": sla_breach_carried(escs, now),
            "workflow": run_workflow(scratch, now=now),
            "workflow_with_existing_issue": run_workflow(scratch, existing_issues='[{"number": 1}]', now=now),
        }
        result["live_state_unchanged"] = LIVE_STATE.read_bytes() == live_before
        return result
    finally:
        if not keep:
            shutil.rmtree(scratch, ignore_errors=True)


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--now", default=None, help="evaluation time (ISO-8601 UTC); default: now")
    p.add_argument("--keep", default=None, help="keep the scratch copy in this directory")
    a = p.parse_args(argv)
    now = _parse(a.now) if a.now else datetime.now(timezone.utc).replace(microsecond=0)
    print(json.dumps(dry_run(now, a.keep), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
