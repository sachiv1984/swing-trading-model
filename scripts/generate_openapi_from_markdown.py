import os
import re
import json
from pathlib import Path
from datetime import datetime

try:
    import yaml  # pip install pyyaml
except ImportError:
    raise SystemExit("Missing dependency: pyyaml. Install with: pip install pyyaml")


ROOT = Path(__file__).resolve().parents[1]
API_DIR = ROOT / "specs" / "api_contracts"
OUT_FILE = ROOT / "docs" / "reference" / "openapi.yaml"

README = API_DIR / "README.md"
CONVENTIONS = API_DIR / "conventions.md"


METHODS = {"get", "post", "put", "patch", "delete"}
ENDPOINT_HEADER_RE = re.compile(r"^##\s+(GET|POST|PUT|PATCH|DELETE)\s+(.+?)\s*$", re.IGNORECASE)
CODEBLOCK_JSON_RE = re.compile(r"```json\s*(.*?)\s*```", re.DOTALL | re.IGNORECASE)

CONTRACT_VERSION_RE = re.compile(r"Contract version:\s*([0-9]+\.[0-9]+\.[0-9]+)", re.IGNORECASE)

HEALTH_PATHS = {"/health", "/health/detailed", "/test/endpoints"}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_contract_version(readme_text: str) -> str:
    m = CONTRACT_VERSION_RE.search(readme_text)
    return m.group(1) if m else "0.0.0"


def guess_tag_from_filename(filename: str) -> str:
    # portfolio_endpoints.md -> Portfolio, position_endpoints.md -> Positions, etc.
    base = filename.replace("_endpoints.md", "")
    base = base.replace("_", " ")
    return base.title()


def safe_json_load(s: str):
    try:
        return json.loads(s)
    except Exception:
        return None


def json_example_to_schema(example):
    """
    Very lightweight schema inference from example JSON.
    Produces an OpenAPI schema object with types but minimal constraints.
    """
    if example is None:
        return {"type": "object"}

    if isinstance(example, dict):
        props = {}
        required = []
        for k, v in example.items():
            required.append(k)
            props[k] = json_example_to_schema(v)
        return {"type": "object", "properties": props, "required": required}

    if isinstance(example, list):
        item_schema = json_example_to_schema(example[0]) if example else {"type": "object"}
        return {"type": "array", "items": item_schema}

    if isinstance(example, bool):
        return {"type": "boolean"}

    if isinstance(example, int):
        return {"type": "integer"}

    if isinstance(example, float):
        return {"type": "number"}

    if isinstance(example, str):
        # basic date-time heuristic
        if re.match(r"^\d{4}-\d{2}-\d{2}T", example):
            return {"type": "string", "format": "date-time"}
        if re.match(r"^\d{4}-\d{2}-\d{2}$", example):
            return {"type": "string", "format": "date"}
        return {"type": "string"}

    return {"type": "string"}


def extract_first_json_example(section_text: str):
    blocks = CODEBLOCK_JSON_RE.findall(section_text)
    for b in blocks:
        ex = safe_json_load(b.strip())
        if ex is not None:
            return ex
    return None


def parse_endpoints(md_text: str, tag: str):
    """
    Parses endpoint sections headed by: ## METHOD /path
    Returns list of (method, path, operation_dict)
    """
    lines = md_text.splitlines()
    endpoints = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()
        m = ENDPOINT_HEADER_RE.match(line)
        if not m:
            i += 1
            continue

        method = m.group(1).lower()
        path = m.group(2).strip()

        # Capture section until next endpoint header or EOF
        start = i + 1
        i += 1
        while i < len(lines) and not ENDPOINT_HEADER_RE.match(lines[i].strip()):
            i += 1
        section = "\n".join(lines[start:i])

        # Summary: use first non-empty line under Purpose/Overview if present
        summary = None
        for sline in section.splitlines():
            s = sline.strip()
            if not s:
                continue
            # Skip headings and separators
            if s.startswith("#") or s.startswith("---"):
                continue
            # Use first meaningful sentence
            summary = s.replace("**", "")
            break
        if not summary:
            summary = f"{method.upper()} {path}"

        # Status codes: detect "Response (200)" etc.
        status_codes = set(re.findall(r"Response\s*\((\d{3})\)", section, re.IGNORECASE))
        # Also detect explicit error mentions like "- `400` ..."
        status_codes.update(re.findall(r"`(\d{3})`", section))
        # Keep only plausible HTTP codes
        status_codes = {c for c in status_codes if c.isdigit() and 100 <= int(c) <= 599}
        if "200" not in status_codes:
            status_codes.add("200")

        # Example response
        example = extract_first_json_example(section)
        schema = json_example_to_schema(example) if example is not None else {"type": "object"}

        # Envelope handling:
        # - Health endpoints are exceptions (non-envelope)
        # - Otherwise default to standard envelope if it looks like it
        use_envelope = path not in HEALTH_PATHS

        if use_envelope:
            # If example appears to already be {status, data}, keep it as-is schema-wise.
            # Otherwise wrap the schema under {status, data}
            if isinstance(example, dict) and "status" in example and "data" in example:
                response_schema = schema
                response_example = example
            else:
                response_schema = {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "enum": ["ok"]},
                        "data": schema
                    },
                    "required": ["status", "data"]
                }
                response_example = {"status": "ok", "data": example} if example is not None else {"status": "ok", "data": {}}
        else:
            response_schema = schema
            response_example = example if example is not None else {}

        responses = {}
        for code in sorted(status_codes, key=lambda x: int(x)):
            if code == "200":
                responses[code] = {
                    "description": "Success",
                    "content": {
                        "application/json": {
                            "schema": response_schema,
                            "example": response_example
                        }
                    }
                }
            else:
                # Generic error structure (canonical shape is described in conventions.md)
                responses[code] = {
                    "description": "Error",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "status": {"type": "string", "enum": ["error"]},
                                    "message": {"type": "string"}
                                },
                                "required": ["status", "message"]
                            }
                        }
                    }
                }

        operation = {
            "tags": [tag],
            "summary": summary,
            "responses": responses,
        }

        endpoints.append((method, path, operation))

    return endpoints


def main():
    if not API_DIR.exists():
        raise SystemExit(f"API contracts folder not found: {API_DIR}")

    version = extract_contract_version(read_text(README)) if README.exists() else "0.0.0"

    # Base OpenAPI skeleton
    spec = {
        "openapi": "3.0.3",
        "info": {
            "title": "Momentum Trading Assistant API (Generated)",
            "version": version,
            "description": (
                "Generated OpenAPI reference derived from canonical Markdown contracts in /specs/api_contracts/. "
                "Canonical truth lives in the Markdown contracts. This file must not be edited manually."
            )
        },
        "servers": [
            {"url": "https://api.example.com", "description": "Production server"},
            {"url": "http://localhost:8000", "description": "Development server"}
        ],
        "paths": {},
    }

    # Parse all *_endpoints.md files
    md_files = sorted(API_DIR.glob("*_endpoints.md"))
    all_eps = []
    for f in md_files:
        tag = guess_tag_from_filename(f.name)
        all_eps.extend(parse_endpoints(read_text(f), tag))

    # Build paths
    for method, path, operation in all_eps:
        spec["paths"].setdefault(path, {})
        spec["paths"][path][method] = operation

    # Ensure output folder exists
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Write YAML
    generated_at = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    header_comment = (
        "# -------------------------------------------------------------------\n"
        "# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY\n"
        f"# Generated from: /specs/api_contracts/*_endpoints.md at {generated_at}\n"
        "# Canonical truth: /specs/api_contracts/\n"
        "# -------------------------------------------------------------------\n"
    )

    with OUT_FILE.open("w", encoding="utf-8") as fh:
        fh.write(header_comment)
        yaml.safe_dump(spec, fh, sort_keys=False, allow_unicode=True)

    print(f"Wrote: {OUT_FILE}")


if __name__ == "__main__":
    main()
