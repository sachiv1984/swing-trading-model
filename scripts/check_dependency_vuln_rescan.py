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
    if pip_findings:
        lines.append("| Package | Version | Advisory ID | New? |")
        lines.append("|---------|---------|-------------|------|")
        for p, v, i in pip_findings:
            lines.append(f"| `{p}` | `{v}` | `{i}` | {'YES' if i not in known_pip_ids else 'known'} |")
    else:
        lines.append("No pip-audit findings (or tool/output unavailable).")

    lines += [
        "",
        f"### npm audit (high/critical only): {len(npm_findings)} package(s) total, {len(new_npm)} with new advisory IDs (not in baseline)",
    ]
    if npm_findings:
        lines.append("| Package | Severity | Advisory ID(s) | New? |")
        lines.append("|---------|----------|-----------------|------|")
        for p, s, ids in npm_findings:
            has_own_advisory = any(i.startswith("GHSA-") for i in ids)
            is_new = any(i in new_npm_ids for i in ids if i.startswith("GHSA-"))
            status = 'YES' if is_new else ('known' if has_own_advisory else 'n/a')
            lines.append(f"| `{p}` | {s} | {', '.join(f'`{i}`' for i in ids)} | {status} |")
    else:
        lines.append("No npm audit high/critical findings (or tool/output unavailable).")

    lines += [
        "",
        f"### Summary: {new_finding_count} new finding(s) not present in `docs/security/dependency_vuln_baseline.json`",
    ]
    if new_finding_count == 0:
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

    return 0


if __name__ == "__main__":
    sys.exit(main())
