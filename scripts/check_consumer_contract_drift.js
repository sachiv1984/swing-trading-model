#!/usr/bin/env node
/**
 * Consumer-driven contract check (ST-12, EPIC-03, v7.10, BLG-QA-128).
 *
 * Lightweight, scripted check comparing frontend API call sites (the
 * central `api` object in src/api/base44Client.js) against the response
 * fields documented in docs/specs/api_contracts/*.md, to catch cases where
 * a component depends on a field the contract doesn't document (or has
 * stopped documenting).
 *
 * Scope (deliberately bounded, per this story's "lightweight" AC):
 * - Only covers call sites that go through the central `api` object.
 *   Components that construct fetch() calls directly (bypassing api.js)
 *   are a separate, already-tracked concern (see backend_engineering_patterns.md
 *   §Error-response envelope conformance's note on direct URL construction)
 *   and are out of scope for this first pass.
 * - Field-consumption detection is a regex heuristic, not full AST/type
 *   analysis: it reliably catches destructuring at the call site
 *   (`const { a, b } = await api.x.y()`) and simple `variable.field` access
 *   within a bounded line window after the call. It will miss deeply
 *   indirect consumption (field passed through several function calls
 *   before being read) — false negatives are expected and acceptable for
 *   a lightweight check; false positives are manually triaged below.
 *
 * Usage: node scripts/check_consumer_contract_drift.js
 */

const fs = require("fs");
const path = require("path");

const REPO_ROOT = path.resolve(__dirname, "..");
const API_CLIENT_PATH = path.join(REPO_ROOT, "src/api/base44Client.js");
const CONTRACTS_DIR = path.join(REPO_ROOT, "docs/specs/api_contracts");
const SRC_DIRS = [path.join(REPO_ROOT, "src/pages"), path.join(REPO_ROOT, "src/components")];

function walk(dir, out = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full, out);
    else if (entry.name.endsWith(".js")) out.push(full);
  }
  return out;
}

function normalizePath(p) {
  return p
    .replace(/\$\{[^}]+\}/g, "*")
    .replace(/\{[^}]+\}/g, "*")
    .split("?")[0]
    .replace(/\/$/, "");
}

// --- Step 1: parse api.<category>.<method> -> HTTP path template ---
function parseApiClient() {
  const text = fs.readFileSync(API_CLIENT_PATH, "utf8");
  const startIdx = text.indexOf("export const api = {");
  if (startIdx === -1) throw new Error("Could not find `export const api = {` in base44Client.js");
  // Find the matching closing brace for this object literal by brace counting.
  let depth = 0, i = startIdx + "export const api = ".length, end = -1;
  for (; i < text.length; i++) {
    if (text[i] === "{") depth++;
    else if (text[i] === "}") {
      depth--;
      if (depth === 0) { end = i; break; }
    }
  }
  const apiBlock = text.slice(startIdx, end + 1);

  const endpoints = [];
  const categoryRe = /(\w+):\s*\{/g;
  let catMatch;
  while ((catMatch = categoryRe.exec(apiBlock)) !== null) {
    const category = catMatch[1];
    const catStart = catMatch.index + catMatch[0].length;
    // find this category's closing brace
    let d = 1, j = catStart, catEnd = -1;
    for (; j < apiBlock.length; j++) {
      if (apiBlock[j] === "{") d++;
      else if (apiBlock[j] === "}") { d--; if (d === 0) { catEnd = j; break; } }
    }
    const catBody = apiBlock.slice(catStart, catEnd);
    const methodRe = /(\w+):\s*async[^(]*\([^)]*\)\s*=>[\s\S]*?doFetch\(\s*[`'"]([^`'"]+)[`'"]/g;
    let m;
    while ((m = methodRe.exec(catBody)) !== null) {
      const method = m[1];
      const rawPath = m[2];
      endpoints.push({
        category, method, callSite: `api.${category}.${method}`,
        pathTemplate: normalizePath(rawPath),
      });
    }
  }
  return endpoints;
}

// --- Step 2: parse contract docs -> {httpMethod, pathTemplate} -> Set(fields) ---
function parseContracts() {
  const contractFields = new Map(); // key: "METHOD /path" (normalized) -> Set(fields)
  const files = fs.readdirSync(CONTRACTS_DIR).filter((f) => f.endsWith(".md"));
  for (const file of files) {
    const text = fs.readFileSync(path.join(CONTRACTS_DIR, file), "utf8");
    const headingRe = /^## (GET|POST|PUT|PATCH|DELETE) (\/\S+)/gm;
    let m;
    const headingMatches = [...text.matchAll(headingRe)];
    for (let idx = 0; idx < headingMatches.length; idx++) {
      const [full, httpMethod, rawPath] = headingMatches[idx];
      const sectionStart = headingMatches[idx].index;
      const sectionEnd = idx + 1 < headingMatches.length ? headingMatches[idx + 1].index : text.length;
      const section = text.slice(sectionStart, sectionEnd);
      // Response fields, not request fields: find a "### Response" sub-heading
      // (several spelling variants exist across contract files) and take the
      // first ```json block after it, not the first one in the whole section
      // (which is usually the request body example).
      const responseHeadingMatch = section.match(/###\s*Response[^\n]*\n/i);
      const searchFrom = responseHeadingMatch
        ? section.slice(responseHeadingMatch.index + responseHeadingMatch[0].length)
        : section;
      const jsonBlockMatch = searchFrom.match(/```json\n([\s\S]*?)```/);
      if (!jsonBlockMatch) continue;
      let fields = new Set();
      try {
        const parsed = JSON.parse(jsonBlockMatch[1]);
        const collect = (obj, depth) => {
          if (!obj || typeof obj !== "object" || depth > 1) return;
          for (const k of Object.keys(obj)) {
            fields.add(k);
            if (k === "data" && obj[k] && typeof obj[k] === "object" && !Array.isArray(obj[k])) {
              collect(obj[k], depth + 1);
            }
          }
        };
        collect(parsed, 0);
      } catch {
        continue; // not strict JSON (comments, trailing content) — skip, lightweight check
      }
      const key = `${httpMethod} ${normalizePath(rawPath)}`;
      const existing = contractFields.get(key) || new Set();
      fields.forEach((f) => existing.add(f));
      contractFields.set(key, existing);
    }
  }
  return contractFields;
}

// --- Step 3: scan src/pages + src/components for api.category.method() call sites ---
//
// Two dominant consumption patterns in this codebase:
//   (A) Direct await: `const { a, b } = await api.x.y(...)` or
//       `const result = await api.x.y(...); result.field`
//   (B) @tanstack/react-query: `const { data: alias } = useQuery({ queryFn:
//       () => api.x.y(...), select: (data) => ... })` — the destructured
//       alias (or bare `data`) is used elsewhere in the component; if a
//       `select` transform is present, its own parameter is what actually
//       touches the raw response fields.
function findCallSitesAndFields(endpoints) {
  const byCallSite = new Map(endpoints.map((e) => [e.callSite, e]));
  const findings = [];

  for (const dir of SRC_DIRS) {
    if (!fs.existsSync(dir)) continue;
    for (const file of walk(dir)) {
      const text = fs.readFileSync(file, "utf8");
      const lines = text.split("\n");

      for (let i = 0; i < lines.length; i++) {
        for (const [callSite, endpoint] of byCallSite) {
          if (!lines[i].includes(callSite + "(")) continue;

          const consumed = new Set();

          // Pattern A1: destructuring at the call site.
          const destructureMatch = lines[i].match(/const\s*\{([^}]+)\}\s*=\s*(?:await\s+)?[\w.]+\(/);
          if (destructureMatch) {
            destructureMatch[1].split(",").forEach((f) => {
              const name = f.split(":")[0].trim();
              if (name) consumed.add(name);
            });
          }
          // Pattern A2: const varName = await api.x.y(...); varName.field later in file.
          const varMatch = lines[i].match(/const\s+(\w+)\s*=\s*(?:await\s+)?[\w.]+\(/);
          if (varMatch) {
            collectFieldAccess(lines, i, lines.length, varMatch[1], consumed);
          }

          // Pattern B: react-query useQuery(...) wrapping this call.
          // Search backwards for the nearest `const { ... } = useQuery({` (or
          // `const alias = useQuery(...)`) that opened before this line, and
          // forwards for that same useQuery(...) call's closing paren to find
          // an optional `select: (param) => ...` transform in between.
          const queryBlock = findEnclosingUseQuery(lines, i);
          if (queryBlock) {
            const { destructured, selectParam, blockEndLine } = queryBlock;
            if (selectParam) {
              // Fields are consumed inside the select transform itself.
              collectFieldAccess(lines, i, blockEndLine + 1, selectParam, consumed);
            }
            if (destructured && destructured !== "data") {
              // Aliased (`data: alias`) — alias is consumed elsewhere in the file.
              collectFieldAccess(lines, blockEndLine, lines.length, destructured, consumed);
            } else if (destructured === "data") {
              collectFieldAccess(lines, blockEndLine, lines.length, "data", consumed);
            }
          }

          if (consumed.size > 0) {
            findings.push({
              file: path.relative(REPO_ROOT, file),
              line: i + 1,
              callSite,
              endpoint,
              consumed: [...consumed],
            });
          }
        }
      }
    }
  }
  return findings;
}

// Built-in Array/Object/String/Promise prototype members — never real API
// response fields, but frequently caught by the `varName.word` regex (e.g.
// `positions.map(...)`, `trades.length`, `data.filter(...)`). Excluded to
// keep the report's signal-to-noise ratio usable for a "lightweight" check.
const JS_BUILTIN_MEMBERS = new Set([
  "map", "filter", "reduce", "reduceRight", "forEach", "find", "findIndex",
  "some", "every", "length", "includes", "indexOf", "lastIndexOf", "slice",
  "splice", "sort", "reverse", "concat", "join", "push", "pop", "shift",
  "unshift", "flat", "flatMap", "fill", "copyWithin", "entries", "keys",
  "values", "toString", "valueOf", "hasOwnProperty", "then", "catch",
  "finally", "constructor", "isArray",
]);

function collectFieldAccess(lines, fromLine, toLine, varName, consumed) {
  const fieldRe = new RegExp(`\\b${varName}(?:\\s*\\|\\|[^)]*)?\\)?\\??\\.(\\w+)`, "g");
  const windowEnd = Math.min(lines.length, toLine);
  for (let w = Math.max(0, fromLine); w < windowEnd; w++) {
    let fm;
    while ((fm = fieldRe.exec(lines[w])) !== null) {
      if (!JS_BUILTIN_MEMBERS.has(fm[1])) consumed.add(fm[1]);
    }
  }
}

function findEnclosingUseQuery(lines, callLineIdx) {
  // Search backwards up to 40 lines for the useQuery( opening this block.
  let queryStartLine = -1;
  for (let b = callLineIdx; b >= Math.max(0, callLineIdx - 40); b--) {
    if (/=\s*useQuery\(/.test(lines[b]) || /^\s*useQuery\(/.test(lines[b])) { queryStartLine = b; break; }
  }
  if (queryStartLine === -1) return null;

  // Destructuring is on the `const {...} = useQuery(` line (or a few lines above it).
  let destructured = null;
  for (let b = queryStartLine; b >= Math.max(0, queryStartLine - 10); b--) {
    const m = lines[b].match(/const\s*\{([^}]*)\}\s*=\s*useQuery\(/) || lines[b].match(/data:\s*(\w+)/);
    if (lines[b].includes("= useQuery(")) {
      const dm = lines.slice(Math.max(0, b - 8), b + 1).join("\n").match(/data:\s*(\w+)/);
      destructured = dm ? dm[1] : (lines.slice(Math.max(0, b - 8), b + 1).join("\n").includes("data") ? "data" : null);
      break;
    }
  }

  // Find the useQuery(...) call's closing paren by paren-depth counting from queryStartLine.
  const fullText = lines.join("\n");
  const startOffset = lines.slice(0, queryStartLine).join("\n").length + 1 + lines[queryStartLine].indexOf("useQuery(");
  let depth = 0, k = startOffset + "useQuery".length, endOffset = -1;
  for (; k < fullText.length; k++) {
    if (fullText[k] === "(") depth++;
    else if (fullText[k] === ")") { depth--; if (depth === 0) { endOffset = k; break; } }
  }
  const blockEndLine = endOffset === -1 ? callLineIdx + 20 : fullText.slice(0, endOffset).split("\n").length - 1;
  const blockText = endOffset === -1 ? "" : fullText.slice(startOffset, endOffset);
  const selectMatch = blockText.match(/select:\s*\(\s*(\w+)\s*\)\s*=>/);

  return { destructured, selectParam: selectMatch ? selectMatch[1] : null, blockEndLine };
}

function main() {
  const endpoints = parseApiClient();
  const contracts = parseContracts();
  const findings = findCallSitesAndFields(endpoints);

  const report = [];
  for (const finding of findings) {
    const key = `${finding.endpoint.httpMethodGuess || guessHttpMethod(finding.file, finding.callSite)} ${finding.endpoint.pathTemplate}`;
    // We don't reliably know the HTTP method from api.js alone for all cases;
    // try GET first (most common), then any method for this path.
    let documented = contracts.get(`GET ${finding.endpoint.pathTemplate}`);
    if (!documented) {
      for (const [k, v] of contracts) {
        if (k.endsWith(` ${finding.endpoint.pathTemplate}`)) { documented = v; break; }
      }
    }
    if (!documented) {
      report.push({ ...finding, status: "no-contract-doc-found", undocumentedFields: [] });
      continue;
    }
    const undocumented = finding.consumed.filter((f) => !documented.has(f));
    report.push({
      ...finding,
      status: undocumented.length > 0 ? "MISMATCH" : "ok",
      undocumentedFields: undocumented,
      documentedFields: [...documented],
    });
  }

  const mismatches = report.filter((r) => r.status === "MISMATCH");
  const noDoc = report.filter((r) => r.status === "no-contract-doc-found");

  console.log(`Consumer-driven contract check — ${findings.length} call sites analysed across src/pages + src/components`);
  console.log(`  ${report.length - mismatches.length - noDoc.length} OK, ${mismatches.length} field mismatches, ${noDoc.length} no contract doc found\n`);

  if (mismatches.length > 0) {
    console.log("=== Field mismatches (frontend consumes a field not found in the contract doc) ===");
    for (const r of mismatches) {
      console.log(`  ${r.file}:${r.line} [${r.callSite}] consumes ${JSON.stringify(r.undocumentedFields)} not in documented fields ${JSON.stringify(r.documentedFields)}`);
    }
  }
  if (noDoc.length > 0) {
    console.log("\n=== No contract doc found (endpoint or path not documented in docs/specs/api_contracts/) ===");
    const seen = new Set();
    for (const r of noDoc) {
      const k = r.endpoint.pathTemplate;
      if (seen.has(k)) continue;
      seen.add(k);
      console.log(`  ${r.callSite} -> ${r.endpoint.pathTemplate}`);
    }
  }
}

function guessHttpMethod() { return null; }

main();
