#!/usr/bin/env python3
"""ST-04 (BLG-SEC-15, EPIC-02, v8.5) — combine pip-audit and npm audit JSON
output into a single report, compare HIGH/CRITICAL findings against the
tracked baseline, and emit outputs for the calling workflow.

Usage:
    check_dependency_vuln_rescan.py \
        --pip-audit-json pip_audit_results.json \
        --npm-audit-json npm_audit_results.json \
        --baseline docs/security/dependency_vuln_baseline.json \
        --summary-out rescan_summary.md \
        --github-output "$GITHUB_OUTPUT"

Exit code is always 0 — this script is a reporting tool, not a merge gate
(pip-audit HIGH/CRITICAL enforcement on PRs remains vulnerability-scan.yml's
job; this script serves the independent scheduled cadence).

ST-14 (BLG-SEC-29, EPIC-04, v8.6): a tool-failure scenario (missing
lockfile, non-JSON output, nonzero-exit-with-no-usable-output) previously
produced the exact same visible state as "tool ran, found 0 vulnerabilities"
-- load_json() returning None fed straight into pip_audit_findings()/
npm_audit_findings(), both of which treat None as "no findings" with no
distinguishing signal. This script now emits per-tool `pip_audit_status`/
`npm_audit_status` ("ok"/"failed") to --github-output, and the summary
report states tool failure explicitly rather than folding it into the same
sentence as a genuine zero-findings result. The calling workflow
(dependency-vuln-rescan.yml) fails the job visibly when either status is
"failed", rather than reporting a quiet green "0 findings" run.
"""
import argparse
import json
import sys


def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"::warning::Could not read {path}: {e}", file=sys.stderr)
        return None


def npm_audit_tool_failed(data):
    """True when npm audit ran but reported its own failure rather than a
    real scan result (e.g. missing package-lock.json produces an ENOLOCK
    error object -- valid JSON, but no "vulnerabilities" key at all, which
    npm_audit_findings() would otherwise silently read as zero findings)."""
    return isinstance(data, dict) and "error" in data and "vulnerabilities" not in data


def pip_audit_findings(data):
    """Return list of (package, version, advisory_id) — pip-audit has no
    severity field, so every finding is treated as HIGH/CRITICAL-equivalent
    per vulnerability-scan.yml's own conservative convention."""
    findings = []
    if data is None:
        return findings
    deps = data if isinstance(data, list) else data.get("dependencies", [])
    for dep in deps:
        for vuln in dep.get("vulns", []):
            findings.append((dep.get("name"), dep.get("version"), vuln.get("id", "UNKNOWN")))
    return findings


def npm_audit_findings(data):
    """Return list of (package, severity, [advisory_ids]) for high/critical only.

    npm audit's `via` array holds either advisory dicts (this package has its
    own GHSA advisory) or plain strings (this package is only vulnerable
    because a package it depends on is — no advisory of its own; that
    dependency's finding is reported separately, under its own name). A
    package with only string `via` entries has no independent advisory
    identity, so it must not be assigned a synthetic placeholder ID — a
    placeholder can never appear in the baseline, so it would show as "new"
    on every single run regardless of whether anything actually changed.
    Such packages are still listed (for completeness) but carry no ID and
    are excluded from new-vs-baseline comparison; their risk is captured by
    the underlying named package's own finding.
    """
    findings = []
    if data is None:
        return findings
    vulns = data.get("vulnerabilities", {})
    for name, v in vulns.items():
        sev = v.get("severity")
        if sev not in ("high", "critical"):
            continue
        ids = set()
        inherited_via = []
        for via in v.get("via", []):
            if isinstance(via, dict):
                url = via.get("url", "")
                ids.add(url.rsplit("/", 1)[-1] if url else via.get("title", "?"))
            else:
                inherited_via.append(via)
        if ids:
            findings.append((name, sev, sorted(ids)))
        else:
            label = f"(no own advisory — inherited via {', '.join(inherited_via)})" if inherited_via else "(no own advisory)"
            findings.append((name, sev, [label]))
    return findings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pip-audit-json", required=True)
    ap.add_argument("--npm-audit-json", required=True)
    ap.add_argument("--baseline", required=True)
    ap.add_argument("--summary-out", required=True)
    ap.add_argument("--github-output", required=False)
    args = ap.parse_args()

    pip_data = load_json(args.pip_audit_json)
    npm_data = load_json(args.npm_audit_json)
    baseline = load_json(args.baseline) or {"pip_audit": {"advisory_ids": []}, "npm_audit": {"advisory_ids": []}}

    pip_audit_status = "ok" if pip_data is not None else "failed"
    npm_tool_failed = npm_audit_tool_failed(npm_data)
    npm_audit_status = "failed" if (npm_data is None or npm_tool_failed) else "ok"
    if npm_tool_failed:
        print(f"::warning::npm audit reported a tool error, not a scan result: {npm_data.get('error')}", file=sys.stderr)
        npm_data = None  # do not let npm_audit_findings() read the error object as "0 vulnerabilities"

    known_pip_ids = set(baseline.get("pip_audit", {}).get("advisory_ids", []))
    known_npm_ids = set(baseline.get("npm_audit", {}).get("advisory_ids", []))

    pip_findings = pip_audit_findings(pip_data)
    npm_findings = npm_audit_findings(npm_data)

    new_pip = [(p, v, i) for (p, v, i) in pip_findings if i not in known_pip_ids]
    # Only real GHSA-style IDs participate in new-vs-baseline comparison —
    # "(no own advisory ...)" labels have no independent identity to track.
    npm_advisory_ids = {aid for (_, _, ids) in npm_findings for aid in ids if aid.startswith("GHSA-")}
    new_npm_ids = npm_advisory_ids - known_npm_ids
    new_npm = [
        (p, s, ids) for (p, s, ids) in npm_findings
        if any(i in new_npm_ids for i in ids if i.startswith("GHSA-"))
    ]

    new_finding_count = len(new_pip) + len(new_npm)

    lines = [
        "## Dependency Vulnerability Re-scan Report",
        "",
        "**Tools:** pip-audit (backend/requirements.txt) + npm audit (package-lock.json)",
        f"**Cadence:** monthly scheduled (`dependency-vuln-rescan.yml`) — see `claude/system/shared_standards.md` §20",
        "",
        f"### pip-audit: {len(pip_findings)} finding(s) total, {len(new_pip)} new (not in baseline)",
    ]
    if pip_audit_status == "failed":
        lines.append("⚠️ **pip-audit tool/output FAILED — this run is INCONCLUSIVE for pip-audit, not a genuine 0-finding result.** Check the workflow logs for the underlying error (missing/unreadable output file or invalid JSON).")
    elif pip_findings:
        lines.append("| Package | Version | Advisory ID | New? |")
        lines.append("|---------|---------|-------------|------|")
        for p, v, i in pip_findings:
            lines.append(f"| `{p}` | `{v}` | `{i}` | {'YES' if i not in known_pip_ids else 'known'} |")
    else:
        lines.append("No pip-audit findings — tool ran successfully.")

    lines += [
        "",
        f"### npm audit (high/critical only): {len(npm_findings)} package(s) total, {len(new_npm)} with new advisory IDs (not in baseline)",
    ]
    if npm_audit_status == "failed":
        lines.append("⚠️ **npm audit tool/output FAILED — this run is INCONCLUSIVE for npm audit, not a genuine 0-finding result.** Check the workflow logs for the underlying error (missing lockfile, invalid JSON, or a reported tool error).")
    elif npm_findings:
        lines.append("| Package | Severity | Advisory ID(s) | New? |")
        lines.append("|---------|----------|-----------------|------|")
        for p, s, ids in npm_findings:
            has_own_advisory = any(i.startswith("GHSA-") for i in ids)
            is_new = any(i in new_npm_ids for i in ids if i.startswith("GHSA-"))
            status = 'YES' if is_new else ('known' if has_own_advisory else 'n/a')
            lines.append(f"| `{p}` | {s} | {', '.join(f'`{i}`' for i in ids)} | {status} |")
    else:
        lines.append("No npm audit high/critical findings — tool ran successfully.")

    lines += [
        "",
        f"### Summary: {new_finding_count} new finding(s) not present in `docs/security/dependency_vuln_baseline.json`",
    ]
    if pip_audit_status == "failed" or npm_audit_status == "failed":
        failed_tools = ", ".join(t for t, s in (("pip-audit", pip_audit_status), ("npm audit", npm_audit_status)) if s == "failed")
        lines.append(f"⚠️ **INCONCLUSIVE — {failed_tools} failed this run.** The finding counts above do not represent a complete scan; do not treat this as a clean/0-finding result.")
    elif new_finding_count == 0:
        lines.append("No new HIGH/CRITICAL findings since baseline — no issue filed this run.")
    else:
        lines.append("New findings detected — a GitHub issue has been filed/updated for Cybersecurity & Trust Lead triage.")

    report = "\n".join(lines)
    with open(args.summary_out, "w") as f:
        f.write(report)
    print(report)

    if args.github_output:
        with open(args.github_output, "a") as f:
            f.write(f"new_finding_count={new_finding_count}\n")
            f.write(f"pip_finding_count={len(pip_findings)}\n")
            f.write(f"npm_finding_count={len(npm_findings)}\n")
            f.write(f"pip_audit_status={pip_audit_status}\n")
            f.write(f"npm_audit_status={npm_audit_status}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
