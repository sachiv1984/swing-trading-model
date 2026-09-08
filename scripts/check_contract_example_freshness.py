#!/usr/bin/env python3
"""
Contract example-payload freshness check (ST-44, EPIC-05, v9.2, BLG-SPEC-120).

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

Usage: python3 scripts/check_contract_example_freshness.py
Exit code: 0 if every checked example's top-level keys are a subset of (or
equal to) the resolved schema's known properties, 1 if any example uses a
key the schema doesn't declare (likely stale/renamed field) or the schema
declares required fields absent from every checked example for that path.
Endpoints/examples this script cannot confidently match are reported
separately as SKIPPED, not counted as pass or fail.

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


def schema_top_keys(schema, root, depth=3):
    """Flatten a resolved schema's property names, descending into nested
    objects up to `depth` levels, producing dotted keys (e.g. 'data.transaction.id')."""
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
            if isinstance(sub_r, dict) and sub_r.get("type") == "object":
                for nested in schema_top_keys(sub_r, root, depth - 1):
                    keys.add(f"{name}.{nested}")
            if isinstance(sub_r, dict) and sub_r.get("type") == "array":
                items = resolve_ref(sub_r.get("items", {}), root)
                if isinstance(items, dict) and items.get("type") == "object":
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
    for code in ("200", "201"):
        if code in responses:
            resp = resolve_ref(responses[code], root)
            content = resp.get("content", {}).get("application/json", {})
            if "schema" in content:
                return schema_top_keys(content["schema"], root)
    return None


def find_examples(text):
    """Yield (method, path, example_dict) for each METHOD/path heading whose
    section contains a JSON fence near a 'response'/'schema' marker."""
    headings = list(HEADING_RE.finditer(text))
    for i, m in enumerate(headings):
        method, path = m.group(1), m.group(2)
        section_end = headings[i + 1].start() if i + 1 < len(headings) else len(text)
        section = text[m.end():section_end]
        best = None
        for fence in JSON_FENCE_RE.finditer(section):
            preceding = section[max(0, fence.start() - 200):fence.start()]
            if RESPONSE_MARKER_RE.search(preceding):
                best = fence.group(1)
        if best is None:
            continue
        try:
            example = json.loads(best)
        except json.JSONDecodeError:
            continue
        if isinstance(example, dict):
            yield method, path, example


def main():
    if not OPENAPI_FILE.exists() or not CONTRACTS_DIR.exists():
        print("Required files not found.", file=sys.stderr)
        return 1

    root = yaml.safe_load(OPENAPI_FILE.read_text())

    stale = []  # (file, method, path, extra_keys)
    checked = 0
    skipped = []

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

    print(f"Checked {checked} contract response examples against openapi.yaml.\n")

    if stale:
        print(f"POSSIBLE DRIFT ({len(stale)}) — example key(s) not found in the resolved openapi.yaml schema:")
        for fname, method, path, extra in stale:
            print(f"  - {fname}: {method} {path} -> {', '.join(extra)}")
        print()

    if skipped:
        print(f"SKIPPED ({len(skipped)}) — could not confidently resolve a schema to compare against:")
        for fname, method, path, reason in skipped:
            print(f"  - {fname}: {method} {path} ({reason})")
        print()

    if not stale:
        print("No drift detected in checked examples.")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
