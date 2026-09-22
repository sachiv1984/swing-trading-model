#!/usr/bin/env python3
"""
CI minutes and artifact-storage visibility (ST-17, BLG-OPS-165, EPIC-04, v9.6).

Produces a monthly per-workflow report of GitHub Actions run minutes and
artifact storage. Cost visibility already covers AI and hosting spend
(docs/ops/cloud_infra_spend_by_epic.md, claude_cost_review_2026-05.md, etc.)
but not CI minutes, which grew with the Playwright shard increase 4->8
(v9.3) with nothing tracking it.

"Billable minutes", not billable here (public-repo finding, confirmed
live 2026-09-22): this repository is public (`"private": false`), and
GitHub Actions does not meter or bill minutes on public repositories --
confirmed by inspecting GET /repos/{owner}/{repo}/actions/runs/{run_id}/timing
directly: `billable.UBUNTU.total_ms` is `0` for every run sampled, while
the same response's own `run_duration_ms` field (wall-clock run time,
unaffected by billing status) is populated normally. This script therefore
tracks `run_duration_ms` -- labelled "run minutes" throughout, deliberately
not "billable minutes" -- as the closest available proxy for CI resource
consumption and capacity trend. It has no dollar-cost meaning for this
repo today, but is the correct metric to watch if the repo ever goes
private (Actions minutes are metered per the private-repo plan's included
quota from that point on) and is still a real signal of shard-count/
schedule-frequency growth either way.

Access note: the repo-scoped `gh` CLI token separately cannot read the
account-level GitHub Actions billing API (GET /users/{user}/settings/
billing/actions returns 403 "Resource not accessible by personal access
token", confirmed live 2026-09-22) -- that endpoint needs a token with the
`plan` scope, which sprint-execution sessions do not carry. This script
does not need it: the per-workflow runs-list endpoint and the per-run
timing endpoint both work with ordinary repo Actions-read access.

Sampling, disclosed (not a full census): this repo accumulates several
thousand workflow runs per calendar month (confirmed live: 9958 runs in
August 2026 alone, across ~45 scheduled/dispatched workflows). Calling
/timing on every single run would be several thousand API calls per
report -- impractical against GitHub's REST rate limit and CI job time
budget for a monthly report. Instead, for each workflow this script takes
the exact run count for the window (one cheap count-only list call per
workflow) and estimates run minutes from the wall-clock duration of a
bounded sample of that workflow's most recent runs (default 5) --
`avg_minutes_per_run * exact_run_count`. The report clearly labels this
`estimated_minutes` and states the sample size per row, per the
disclose-rather-than-fabricate convention (precedent: ESC-EXEC-20260910-01).
Artifact storage, by contrast, is an exact figure at report-generation
time: it comes from a single paginated listing of currently-live artifacts
(bounded by each upload's own retention-days, not by run volume) filtered
to the window and mapped to a workflow by its artifact-name prefix (the 6
known upload steps across 4 workflow files -- see
ARTIFACT_NAME_PREFIX_TO_WORKFLOW) -- see the undercount caveat this script
prints when a window has aged past a short retention-days value.

Pure logic (`estimate_workflow_minutes`, `aggregate_artifact_storage`,
`workflow_for_artifact_name`, `artifact_undercount_caveat`) takes plain
already-fetched values and does no I/O, so it is unit-tested directly
(tests/test_ci_usage_report.py) without mocking `gh`.

Usage:
    python3 scripts/generate_ci_usage_report.py [--year-month YYYY-MM] [--sample-size N] [--out PATH]

Requires the `gh` CLI to be authenticated (same precondition as every other
`gh api` call this routine makes). Defaults to the previous full UTC
calendar month if --year-month is omitted.
"""
import argparse
import calendar
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = "sachiv1984/swing-trading-model"
DEFAULT_SAMPLE_SIZE = 5

# Every known upload-artifact step's `name:` value, by prefix, mapped to its
# parent workflow's own top-level `name:` (as GitHub Actions displays it).
# Re-derive with `grep -rn "uses: actions/upload-artifact" .github/workflows/*.yml`
# plus reading each `with: name:` if this mapping may be stale.
ARTIFACT_NAME_PREFIX_TO_WORKFLOW = {
    "playwright-report-shard": "Playwright E2E Acceptance Tests",
    "visual-snapshot-report": "Playwright E2E Acceptance Tests",
    "visual-regression-report": "Playwright E2E Acceptance Tests",
    "smoke-test-report": "Critical-Path Smoke Tests (Playwright)",
    "db-backup-": "Production Database Backup",
    "updated-visual-snapshots": "Update Visual Snapshot Baselines",
}

# Each prefix's own `retention-days:` (.github/workflows/*.yml), used only to
# compute the report's undercount caveat below -- an artifact whose
# retention has already elapsed by report-generation time is gone from the
# API entirely, not merely hidden, so a window closed longer ago than the
# shortest of these is silently missing some of its artifacts.
ARTIFACT_NAME_PREFIX_TO_RETENTION_DAYS = {
    "playwright-report-shard": 14,
    "visual-snapshot-report": 30,
    "visual-regression-report": 30,
    "smoke-test-report": 14,
    "db-backup-": 90,
    "updated-visual-snapshots": 7,
}


def _gh_api(path, args=None):
    # --method GET is required whenever -f/-F params are present: gh api
    # otherwise defaults a parameterised call to POST, which 404s against
    # a GET-only list/read endpoint (confirmed live 2026-09-22).
    cmd = ["gh", "api", path, "--method", "GET"] + (args or [])
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


def _gh_api_paginated(path, list_key, extra_args=None, per_page=100):
    """Manually paginate via the `page` query param, since `gh api
    --paginate` concatenates consecutive pages' raw JSON with no
    separator for this response shape (confirmed live 2026-09-22: the
    second page's bytes immediately follow the first's on `stdout` with no
    newline, so line-based NDJSON parsing raises "Extra data"). Returns the
    concatenated `list_key` array across all pages."""
    items = []
    page = 1
    while True:
        data = _gh_api(path, (extra_args or []) + ["-f", f"per_page={per_page}", "-f", f"page={page}"])
        batch = data.get(list_key, [])
        items.extend(batch)
        if len(batch) < per_page:
            break
        page += 1
    return items


def previous_month_window(now=None):
    """Return (start_iso_date, end_iso_date, year_month_label) for the
    previous full UTC calendar month, e.g. run in September -> August."""
    now = now or datetime.now(timezone.utc)
    year, month = now.year, now.month
    if month == 1:
        prev_year, prev_month = year - 1, 12
    else:
        prev_year, prev_month = year, month - 1
    last_day = calendar.monthrange(prev_year, prev_month)[1]
    start = f"{prev_year:04d}-{prev_month:02d}-01"
    end = f"{prev_year:04d}-{prev_month:02d}-{last_day:02d}"
    label = f"{prev_year:04d}-{prev_month:02d}"
    return start, end, label


def fetch_workflows():
    """All workflow files in the repo: [{id, name}]."""
    raw = _gh_api_paginated(f"repos/{REPO}/actions/workflows", "workflows")
    return [{"id": wf["id"], "name": wf["name"]} for wf in raw]


def fetch_workflow_run_count_and_sample(workflow_id, start_date, end_date, sample_size=DEFAULT_SAMPLE_SIZE):
    """One cheap list call: exact run count for this workflow in the window
    (from total_count), plus up to `sample_size` of its most recent run ids
    in the window (list endpoint default-sorts newest first)."""
    data = _gh_api(
        f"repos/{REPO}/actions/workflows/{workflow_id}/runs",
        ["-f", f"created={start_date}..{end_date}", "-f", f"per_page={sample_size}"],
    )
    total_count = data.get("total_count", 0)
    sample_run_ids = [r["id"] for r in data.get("workflow_runs", [])]
    return total_count, sample_run_ids


def fetch_run_duration_ms(run_id):
    """Wall-clock run duration, not billable time -- see module docstring's
    "Billable minutes, not billable here" note. `billable.*.total_ms` is
    always 0 on this public repo; `run_duration_ms` is the populated field."""
    data = _gh_api(f"repos/{REPO}/actions/runs/{run_id}/timing")
    return data.get("run_duration_ms", 0)


def fetch_artifacts_in_window(start_date, end_date):
    """All currently-live artifacts (bounded by each upload's own
    retention-days, not run volume) whose created_at falls in
    [start_date, end_date]. An artifact whose retention-days has already
    elapsed by the time this script runs is gone from the API entirely --
    see ARTIFACT_NAME_PREFIX_TO_RETENTION_DAYS / the report's own caveat line for the
    resulting undercount risk on a window closed more than ~7 days ago."""
    raw = _gh_api_paginated(f"repos/{REPO}/actions/artifacts", "artifacts")
    start_dt = datetime.fromisoformat(start_date).replace(tzinfo=timezone.utc)
    end_dt = datetime.fromisoformat(end_date).replace(hour=23, minute=59, second=59, tzinfo=timezone.utc)
    artifacts = []
    for artifact in raw:
        created_at = datetime.fromisoformat(artifact["created_at"].replace("Z", "+00:00"))
        if start_dt <= created_at <= end_dt:
            artifacts.append({"name": artifact["name"], "size_in_bytes": artifact.get("size_in_bytes", 0)})
    return artifacts


def estimate_workflow_minutes(sample_duration_ms, total_run_count):
    """Pure -- no I/O.

    sample_duration_ms: list of wall-clock run-duration-ms ints (not
    billable ms -- see module docstring) from a bounded sample of this
    workflow's most recent runs in the window.
    total_run_count: the exact run count for this workflow in the window.

    Returns (avg_minutes_per_run, estimated_total_minutes, sample_size).
    """
    if not sample_duration_ms:
        return 0.0, 0.0, 0
    avg_ms = sum(sample_duration_ms) / len(sample_duration_ms)
    avg_minutes = avg_ms / 60000.0
    return avg_minutes, avg_minutes * total_run_count, len(sample_duration_ms)


def workflow_for_artifact_name(name):
    """Pure. Returns the owning workflow's display name, or None if this
    artifact name doesn't match any known upload step (disclosed as
    "(unmapped artifact)" by the caller, not silently dropped)."""
    for prefix, workflow in ARTIFACT_NAME_PREFIX_TO_WORKFLOW.items():
        if name.startswith(prefix):
            return workflow
    return None


def aggregate_artifact_storage(artifacts):
    """Pure -- no I/O. artifacts: list of {"name": str, "size_in_bytes": int}.
    Returns dict {workflow_name: total_mb} (unmapped names grouped under
    "(unmapped artifact)")."""
    by_workflow = {}
    for a in artifacts:
        workflow = workflow_for_artifact_name(a["name"]) or "(unmapped artifact)"
        by_workflow[workflow] = by_workflow.get(workflow, 0.0) + a["size_in_bytes"] / (1024 * 1024)
    return by_workflow


def artifact_undercount_caveat(days_since_window_end):
    """Pure. Returns a caveat string (possibly empty) about which known
    artifact categories have very likely already expired past their own
    retention-days by the time this window's artifacts were fetched --
    an artifact past retention is deleted by GitHub, not merely hidden, so
    it cannot be recovered by this or any other script once gone."""
    if days_since_window_end is None:
        return ""
    stale = sorted({
        f"{workflow} ({retention}d retention)"
        for prefix, retention in ARTIFACT_NAME_PREFIX_TO_RETENTION_DAYS.items()
        if days_since_window_end > retention
        for workflow in [ARTIFACT_NAME_PREFIX_TO_WORKFLOW[prefix]]
    })
    if not stale:
        return ""
    return (
        f"⚠️ **Artifact undercount risk:** this window closed {days_since_window_end} day(s) before this report was "
        "generated. GitHub deletes an artifact outright once its own `retention-days` elapses — it is not recoverable "
        "by this or any other script — so the artifact-storage figures below for these workflows are very likely "
        f"undercounted (some or all of the window's artifacts have already expired): {', '.join(stale)}. Run this "
        "report promptly after each month closes (the scheduled `ci-usage-report.yml` workflow does) to avoid this."
    )


def render_markdown(report, artifact_by_workflow, year_month_label, sample_size, days_since_window_end=None):
    total_runs = sum(e["run_count"] for e in report.values())
    total_minutes = sum(e["estimated_minutes"] for e in report.values())
    total_artifact_mb = sum(artifact_by_workflow.values())

    lines = [
        f"# CI Minutes and Artifact Storage — {year_month_label}",
        "",
        "**Generated by:** `scripts/generate_ci_usage_report.py` (ST-17, BLG-OPS-165, EPIC-04, v9.6)",
        f"**Window:** full UTC calendar month {year_month_label}",
        "",
        f"**Totals:** {total_runs} runs, ~{total_minutes:.1f} estimated run minutes, {total_artifact_mb:.1f} MB artifact storage (subject to the undercount caveat below, if present).",
        "",
        "**\"Run minutes\", not \"billable minutes\":** this repository is public, and GitHub Actions does not meter or "
        "bill minutes on public repositories (confirmed live: `billable.*.total_ms` is `0` for every run on this repo). "
        "The figures below are wall-clock `run_duration_ms` instead — a real signal of CI resource consumption and "
        "capacity trend, with no dollar-cost meaning today, but the metric to watch if this repo ever goes private.",
        "",
        "**Methodology (disclosed, not a full census):** `run_count` is exact (one count-only API call per workflow). "
        f"`estimated_minutes` is `avg_minutes_per_run * run_count`, where the average is taken from up to {sample_size} "
        "of that workflow's most recent runs in the window (`sample_n` column) — calling the per-run timing endpoint on "
        "every one of several thousand runs/month is impractical within the GitHub REST rate limit. Artifact storage "
        "reflects only artifacts still live at report-generation time (bounded by each upload's own retention-days, "
        "not run volume), mapped to a workflow by its artifact-name prefix.",
    ]
    caveat = artifact_undercount_caveat(days_since_window_end)
    if caveat:
        lines += ["", caveat]
    lines += [
        "",
        "| Workflow | Runs | Sample n | Est. run minutes | Artifact storage (MB) |",
        "|---|---:|---:|---:|---:|",
    ]
    all_workflow_names = set(report.keys()) | set(artifact_by_workflow.keys())
    rows = []
    for name in all_workflow_names:
        entry = report.get(name, {"run_count": 0, "estimated_minutes": 0.0, "sample_size": 0})
        artifact_mb = artifact_by_workflow.get(name, 0.0)
        rows.append((name, entry["run_count"], entry["sample_size"], entry["estimated_minutes"], artifact_mb))
    rows.sort(key=lambda r: r[3], reverse=True)
    for name, run_count, sample_n, minutes, artifact_mb in rows:
        lines.append(f"| {name} | {run_count} | {sample_n} | {minutes:.1f} | {artifact_mb:.1f} |")
    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--year-month", help="YYYY-MM to report on (default: previous full UTC calendar month)")
    parser.add_argument("--sample-size", type=int, default=DEFAULT_SAMPLE_SIZE)
    parser.add_argument("--out", help="Output file path (default: docs/ops/ci_usage_reports/<YYYY-MM>.md)")
    args = parser.parse_args()

    if args.year_month:
        year, month = (int(x) for x in args.year_month.split("-"))
        last_day = calendar.monthrange(year, month)[1]
        start_date = f"{year:04d}-{month:02d}-01"
        end_date = f"{year:04d}-{month:02d}-{last_day:02d}"
        label = args.year_month
    else:
        start_date, end_date, label = previous_month_window()

    workflows = fetch_workflows()
    report = {}
    for wf in workflows:
        total_count, sample_run_ids = fetch_workflow_run_count_and_sample(
            wf["id"], start_date, end_date, args.sample_size
        )
        if total_count == 0:
            continue
        sample_ms = [fetch_run_duration_ms(rid) for rid in sample_run_ids]
        avg_minutes, estimated_minutes, sample_size = estimate_workflow_minutes(sample_ms, total_count)
        report[wf["name"]] = {
            "run_count": total_count,
            "avg_minutes_per_run": avg_minutes,
            "estimated_minutes": estimated_minutes,
            "sample_size": sample_size,
        }

    artifacts = fetch_artifacts_in_window(start_date, end_date)
    artifact_by_workflow = aggregate_artifact_storage(artifacts)

    end_dt = datetime.fromisoformat(end_date).replace(tzinfo=timezone.utc)
    days_since_window_end = (datetime.now(timezone.utc) - end_dt).days

    markdown = render_markdown(report, artifact_by_workflow, label, args.sample_size, days_since_window_end)

    out_path = Path(args.out) if args.out else Path(f"docs/ops/ci_usage_reports/{label}.md")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(markdown)
    print(f"Wrote {out_path} ({len(report)} workflows with runs, {len(artifacts)} artifacts in window)")


if __name__ == "__main__":
    main()
