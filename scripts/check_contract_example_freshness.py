#!/usr/bin/env python3
"""
Contract example-payload freshness check (ST-44, EPIC-05, v9.2, BLG-SPEC-120).
Extended with an error-envelope conformance check (ST-21, EPIC-05, v9.8,
BLG-API-05) -- see the second half of this docstring.

For each `## METHOD /path` heading in a `docs/specs/api_contracts/*.md`
canonical contract file, finds the nearest response example JSON block
(a ```json fence under a heading/line mentioning "Response" or "schema")
and compares its top-level (and one level of nesting) keys against the
`docs/reference/openapi.yaml` response schema for the same method+path,
resolving `$ref` pointers into `components/`.

This is a structural drift *detector*, not an auto-fixer or a live-response
checker: it cannot call the running API (no server/DB access from this
environment — same constraint noted in `docs/ops/anthropic_api_cost_trend_2026.md`
§3), so "live response shape" here means the openapi.yaml contract's own
declared schema, which is itself required to track the real implementation
(CLAUDE.md's same-commit openapi.yaml rule). Drift between openapi.yaml and
the actual running backend is out of this script's scope — that is what
`docs/ops/openapi_3way_sweep_log.md`-style manual sweeps are for.

**Error-envelope check (ST-21, BLG-API-05):** separately, every JSON object
fence that looks like a documented 4xx/5xx error example (see
`find_error_examples`/`BOUNDARY_RE` below) is validated against the fixed
canonical envelope in `conventions.md` §13.1 (`{"status": "error", "message":
"<str>"}`), not against openapi.yaml — the envelope is a codebase-wide
convention, not a per-endpoint schema. `/health`, `/health/detailed`,
`/health/database`, `/test/endpoints` and `/test/rate-limit-scenarios` are
exempt (conventions.md §13.3).

Usage: python3 scripts/check_contract_example_freshness.py
Exit code: 0 if every checked success example's top-level keys are a subset
of (or equal to) the resolved schema's known properties AND every checked
error example matches the canonical envelope; 1 if either check finds a
divergence (an unknown key, or a non-conforming error shape). Endpoints/
examples this script cannot confidently match a success schema for are
reported separately as SKIPPED, not counted as pass or fail (this SKIPPED
category applies only to the openapi.yaml success-schema check, not the
error-envelope check, which has no schema to skip against).

**Scheduled cadence (ST-44 AC):** run manually before any `docs/reference/openapi.yaml`
version bump that touches an endpoint with a contract example (part of the
pre-PR checklist in `commit-check` for API-contract-touching commits), and
at every `run audit` cycle (alongside `check_specs_index_freshness.py`).
Not wired into CI as a hard gate this cycle — flagged results require API
Contracts & Documentation Owner judgment (an example can legitimately show
only a subset of fields for brevity), same posture as the specs-index
freshness check it is modelled on.
"""
import json
import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CONTRACTS_DIR = REPO_ROOT / "docs" / "specs" / "api_contracts"
OPENAPI_FILE = REPO_ROOT / "docs" / "reference" / "openapi.yaml"

HEADING_RE = re.compile(r"^##\s+(GET|POST|PUT|PATCH|DELETE)\s+(/\S+)\s*$", re.M)
JSON_FENCE_RE = re.compile(r"```json\n(.*?)\n```", re.S)
RESPONSE_MARKER_RE = re.compile(r"response|schema", re.I)


def resolve_ref(node, root):
    """Follow a single-level $ref (or a chain of them) against the full doc."""
    seen = 0
    while isinstance(node, dict) and "$ref" in node and seen < 10:
        ref = node["$ref"]
        assert ref.startswith("#/"), f"external $ref unsupported: {ref}"
        target = root
        for part in ref[2:].split("/"):
            target = target[part]
        node = target
        seen += 1
    return node


def _is_object_like(node):
    """True for a plain `type: object` schema OR one composed via
    allOf/oneOf/anyOf with no sibling `type` key (this codebase's own
    convention for extending a base schema, e.g. `Position` = `PositionSummary`
    allOf plus extra properties — see docs/reference/openapi.yaml). Without
    this, the nested-descent checks below (which only tested `type ==
    "object"`) silently failed to descend into any allOf-composed nested
    schema or array-of-allOf-composed-items, undercounting real schema
    properties. Found live at GET /positions/search/tags (ST-26,
    BLG-SPEC-139): its response is `data: Position[]`, and `Position` is
    allOf-composed, so every one of `Position`'s real properties was
    invisible to this script before this fix."""
    return isinstance(node, dict) and (
        node.get("type") == "object"
        or "allOf" in node
        or "oneOf" in node
        or "anyOf" in node
    )


def schema_top_keys(schema, root, depth=3):
    """Flatten a resolved schema's property names, descending into nested
    objects up to `depth` levels, producing dotted keys (e.g. 'data.transaction.id').

    A schema counts as "object-like" for descent purposes if it declares
    `type: object` OR is composed via allOf/oneOf/anyOf (see `_is_object_like`)."""
    schema = resolve_ref(schema, root)
    keys = set()
    if not isinstance(schema, dict):
        return keys
    for combinator in ("allOf", "oneOf", "anyOf"):
        if combinator in schema:
            for sub in schema[combinator]:
                keys |= schema_top_keys(sub, root, depth)
    props = schema.get("properties", {})
    for name, sub in props.items():
        keys.add(name)
        if depth > 1:
            sub_r = resolve_ref(sub, root)
            if _is_object_like(sub_r):
                for nested in schema_top_keys(sub_r, root, depth - 1):
                    keys.add(f"{name}.{nested}")
            if isinstance(sub_r, dict) and sub_r.get("type") == "array":
                items = resolve_ref(sub_r.get("items", {}), root)
                if _is_object_like(items):
                    for nested in schema_top_keys(items, root, depth - 1):
                        keys.add(f"{name}[].{nested}")
    return keys


def json_flatten_keys(obj, prefix="", depth=3):
    keys = set()
    if depth <= 0 or not isinstance(obj, dict):
        return keys
    for k, v in obj.items():
        full = f"{prefix}{k}"
        keys.add(full)
        if isinstance(v, dict):
            keys |= json_flatten_keys(v, prefix=f"{full}.", depth=depth - 1)
        elif isinstance(v, list) and v and isinstance(v[0], dict):
            keys |= json_flatten_keys(v[0], prefix=f"{full}[].", depth=depth - 1)
    return keys


def response_schema_for(root, method, path):
    paths = root.get("paths", {})
    op = None
    # Direct match, then template-parameter match (e.g. /trade-plans/{id}).
    if path in paths:
        op = paths[path].get(method.lower())
    else:
        for cand_path, cand_ops in paths.items():
            pattern = "^" + re.sub(r"\{[^}]+\}", r"[^/]+", cand_path) + "$"
            if re.match(pattern, path) and method.lower() in cand_ops:
                op = cand_ops[method.lower()]
                break
    if op is None:
        return None
    responses = op.get("responses", {})
    # 202 covers async-accepted endpoints (e.g. POST /screener/run) -- found
    # missing here, ST-26/BLG-SPEC-139, v9.5: it was silently treated as
    # SKIPPED (no schema to compare) even where openapi.yaml does declare one.
    for code in ("200", "201", "202"):
        if code in responses:
            resp = resolve_ref(responses[code], root)
            content = resp.get("content", {}).get("application/json", {})
            if "schema" in content:
                return schema_top_keys(content["schema"], root)
    return None


ERROR_MARKER_RE = re.compile(
    r"error|HTTP/1\.1 4\d\d|HTTP/1\.1 5\d\d", re.I
)


def find_examples(text):
    """Yield (method, path, example_dict) for each METHOD/path heading whose
    section contains a JSON fence near a 'response'/'schema' marker.

    Picks the FIRST such fence (nearest to the heading), preferring one whose
    preceding text does not itself look like an error-response marker
    (e.g. "### Error responses", "HTTP/1.1 429 Too Many Requests"). Every
    contract file in this directory documents its primary 2xx response
    before any error-response block (confirmed by inspection, ST-26,
    BLG-SPEC-139) — picking the LAST matching fence in the section (the
    pre-fix behaviour) instead picked up whichever error-response example
    happened to appear last, which both contain the word "response" and so
    both matched RESPONSE_MARKER_RE. That produced most of this script's
    "POSSIBLE DRIFT" false positives (e.g. ai_endpoints.md's 429 rate-limit
    example, `{"status": "error", "message": "..."}`, compared against the
    200 schema instead of the actual 200 example)."""
    headings = list(HEADING_RE.finditer(text))
    for i, m in enumerate(headings):
        method, path = m.group(1), m.group(2)
        section_end = headings[i + 1].start() if i + 1 < len(headings) else len(text)
        section = text[m.end():section_end]
        best = None
        fallback = None
        for fence in JSON_FENCE_RE.finditer(section):
            preceding = section[max(0, fence.start() - 200):fence.start()]
            if RESPONSE_MARKER_RE.search(preceding):
                if fallback is None:
                    fallback = fence.group(1)
                if not ERROR_MARKER_RE.search(preceding):
                    best = fence.group(1)
                    break
        if best is None:
            best = fallback
        if best is None:
            continue
        try:
            example = json.loads(best)
        except json.JSONDecodeError:
            continue
        if isinstance(example, dict):
            yield method, path, example


# ST-21 (BLG-API-05, EPIC-05, v9.8): error-payload envelope conformance check.
#
# Distinct from `find_examples`/`response_schema_for` above (which validate a
# *success* example's keys against openapi.yaml's 200/201/202 schema) --
# this instead validates *error* (4xx/5xx) examples against the fixed
# canonical envelope shape in conventions.md SS13.1 (`{"status": "error",
# "message": "<str>"}`), not against openapi.yaml, since the envelope is a
# codebase-wide convention rather than a per-endpoint schema.
ERROR_CODE_RE = re.compile(r"\b([45]\d{2})\b")

# Local section-boundary markers: a real ATX heading (`## `..`###### `) OR a
# line that STARTS with a bold label (this codebase's dominant convention
# for sub-headers within an endpoint section) -- either bold-only
# (`**Idempotency**`) or a bold label immediately followed by prose on the
# same line (`**Request body (application/json):** exactly one of...`,
# `**Bounds:** at most 100...`). Both forms must count as boundaries: a
# bold-only-line requirement missed the latter, inline-labelled form,
# under-bounding the lookback for a fence that followed one (found live,
# ST-21: replay_endpoints.md's `**Request body (application/json):**`
# paragraph mentions a `400` validation constraint, and without this the
# lookback for the two REQUEST-shape example fences that follow it reached
# back past that paragraph's own boundary to the unrelated `**Idempotency**`
# label above it instead).
BOUNDARY_RE = re.compile(r"^(?:#{1,6}\s.*|\*\*[^\n*]+\*\*.*)$", re.M)

# Health/monitoring endpoints are explicitly exempt from the standard error
# envelope (conventions.md SS13.3) -- they use their own always-200
# monitoring-status shapes (e.g. a nested `"status": "error"` field is a
# component's health status, not this envelope).
ENVELOPE_EXEMPT_PATHS = {"/health", "/health/detailed", "/health/database", "/test/endpoints", "/test/rate-limit-scenarios"}


def find_error_examples(text):
    """Yield (method, path, code, example_dict) for each JSON object fence
    immediately preceded (within the current local block only -- see
    `BOUNDARY_RE`) by an HTTP 4xx/5xx status code number. Unlike
    `find_examples` above (which looks for a "response"/"schema" marker
    near ONE fence per section), this scans EVERY fence in the section,
    since a single endpoint's Errors subsection commonly documents more
    than one error example (e.g. 400 and 404 and 500).

    The lookback is bounded to the nearest preceding boundary line (a real
    heading or a bold-only pseudo-heading), not a fixed character window,
    to avoid picking up an unrelated status-code digit sequence mentioned
    in an earlier, structurally distinct part of the same METHOD/path
    section (e.g. a `**Idempotency**` subsection's prose noting "a
    repeated call ... returns `404`" -- found live, ST-21, where several
    DELETE endpoints' 200-success example was mis-flagged as a 404 error
    example under a fixed-window version of this lookback)."""
    headings = list(HEADING_RE.finditer(text))
    for i, m in enumerate(headings):
        method, path = m.group(1), m.group(2)
        if path in ENVELOPE_EXEMPT_PATHS:
            continue
        section_end = headings[i + 1].start() if i + 1 < len(headings) else len(text)
        section = text[m.end():section_end]
        boundaries = [b.start() for b in BOUNDARY_RE.finditer(section)]
        for fence in JSON_FENCE_RE.finditer(section):
            prior_boundaries = [b for b in boundaries if b < fence.start()]
            boundary_start = prior_boundaries[-1] if prior_boundaries else max(0, fence.start() - 200)
            # Additional 120-char cap (whichever bound is closer to the fence
            # wins): a genuine error-response marker sits immediately above
            # its fence (one heading/bold line + a blank line) -- the
            # boundary match alone is not tight enough on its own.
            lookback_start = max(boundary_start, fence.start() - 120)
            preceding = section[lookback_start:fence.start()]
            # A boundary line describing the REQUEST shape (e.g. "**Request
            # body (application/json):**") is a strong negative signal even
            # when a 4xx/5xx code number happens to appear nearby in that
            # same paragraph (e.g. a request-validation constraint like "is
            # a `400 validation_error`") -- found live, ST-21:
            # replay_endpoints.md's two REQUEST-shape example fences were
            # otherwise mis-flagged this way. A fence following a "request"
            # boundary is never itself a response/error example.
            boundary_line = section[boundary_start:boundary_start + 80]
            if re.search(r"request", boundary_line, re.I):
                continue
            codes = [c for c in ERROR_CODE_RE.findall(preceding) if c[0] in ("4", "5")]
            if not codes:
                continue
            code = codes[-1]
            try:
                example = json.loads(fence.group(1))
            except json.JSONDecodeError:
                continue
            if isinstance(example, dict):
                yield method, path, code, example


def envelope_violation_reasons(example):
    """Return a list of human-readable reasons the example diverges from
    the canonical `{"status": "error", "message": "<str>"}` envelope
    (conventions.md SS13.1). An empty list means conformant. Extra fields
    (e.g. the additive `code` field used by replay_endpoints.md /
    strategy_version_comparison_contract.md) are NOT a violation -- SS13.1
    only fixes the two required fields, not an exhaustive key set."""
    reasons = []
    if example.get("status") != "error":
        reasons.append(f"status={example.get('status')!r} (expected \"error\")")
    message = example.get("message")
    if not isinstance(message, str) or not message.strip():
        reasons.append("missing or empty string \"message\" field")
    return reasons


def main():
    if not OPENAPI_FILE.exists() or not CONTRACTS_DIR.exists():
        print("Required files not found.", file=sys.stderr)
        return 1

    root = yaml.safe_load(OPENAPI_FILE.read_text())

    stale = []  # (file, method, path, extra_keys)
    checked = 0
    skipped = []
    envelope_violations = []  # (file, method, path, code, reasons)
    error_examples_checked = 0

    for md_file in sorted(CONTRACTS_DIR.glob("*.md")):
        text = md_file.read_text(errors="replace")
        for method, path, example in find_examples(text):
            schema_keys = response_schema_for(root, method, path)
            if schema_keys is None:
                skipped.append((md_file.name, method, path, "no matching openapi.yaml operation/schema"))
                continue
            example_keys = json_flatten_keys(example)
            # Contract-file convention shows the *contents* of the envelope's
            # `data` field directly (see e.g. cash_endpoints.md "#### `data`
            # schema"), not re-wrapped in another `data:` layer -- so a
            # schema key of `data.foo` must also match an example key of
            # bare `foo`. Compare against the union of both forms.
            unwrapped = {k[len("data."):] for k in schema_keys if k.startswith("data.")}
            comparable = schema_keys | unwrapped
            extra = {k for k in example_keys if k not in comparable and k.split(".")[0] not in comparable}
            checked += 1
            if extra:
                stale.append((md_file.name, method, path, sorted(extra)))

        # ST-21 (BLG-API-05): error-example envelope conformance, separate
        # from the success-example vs. openapi.yaml check above.
        for method, path, code, example in find_error_examples(text):
            error_examples_checked += 1
            reasons = envelope_violation_reasons(example)
            if reasons:
                envelope_violations.append((md_file.name, method, path, code, reasons))

    print(f"Checked {checked} contract response examples against openapi.yaml.")
    print(f"Checked {error_examples_checked} contract error-response examples against the canonical envelope (conventions.md §13.1).\n")

    if stale:
        print(f"POSSIBLE DRIFT ({len(stale)}) — example key(s) not found in the resolved openapi.yaml schema:")
        for fname, method, path, extra in stale:
            print(f"  - {fname}: {method} {path} -> {', '.join(extra)}")
        print()

    if envelope_violations:
        print(f"ERROR ENVELOPE DRIFT ({len(envelope_violations)}) — error example(s) diverge from the canonical `{{\"status\": \"error\", \"message\": \"...\"}}` envelope:")
        for fname, method, path, code, reasons in envelope_violations:
            print(f"  - {fname}: {method} {path} ({code}) -> {'; '.join(reasons)}")
        print()

    if skipped:
        print(f"SKIPPED ({len(skipped)}) — could not confidently resolve a schema to compare against:")
        for fname, method, path, reason in skipped:
            print(f"  - {fname}: {method} {path} ({reason})")
        print()

    if not stale and not envelope_violations:
        print("No drift detected in checked examples.")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
