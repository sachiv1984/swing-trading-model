#!/usr/bin/env python3
"""
@babel/parser differential for scripts/check_ui_copy_forbidden_phrases.py
(ST-18, BLG-QA-194, EPIC-03, v9.9).

The UI-copy boundary lint is a dependency-free tokeniser, not a JS parser. This manual
check parses every file the lint scans with a real parser (@babel/parser, already in
node_modules via the frontend toolchain) and compares the two:

  - literal coverage: how many of babel's string literals, template parts, JSX text
    nodes and JSX attribute strings the tokeniser also extracted (after the same
    normalisation), with a sample of the ones it did not
  - missed phrase hits (the figure that matters): every literal in which babel's text
    contains a forbidden §13.2 phrase must also be a lint hit in the same file. Any
    miss is printed and the exit code is 1.

Not a CI step (it needs Node and node_modules); run it after changing the tokeniser:
    python3 scripts/ui_copy_lint_babel_differential.py
"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import check_ui_copy_forbidden_phrases as lint  # noqa: E402

REPO_ROOT = Path(__file__).parent.parent

_NODE_EXTRACTOR = r"""
const fs = require('fs');
const parser = require('@babel/parser');
const files = JSON.parse(fs.readFileSync(0, 'utf8'));
const out = {};
for (const file of files) {
  const lits = [];
  let ast;
  try {
    ast = parser.parse(fs.readFileSync(file, 'utf8'), {
      sourceType: 'unambiguous', errorRecovery: true,
      plugins: ['jsx', 'classProperties', 'optionalChaining', 'nullishCoalescingOperator', 'dynamicImport'],
    });
  } catch (e) { out[file] = {error: String(e)}; continue; }
  (function walk(node) {
    if (!node || typeof node.type !== 'string') return;
    if (node.type === 'StringLiteral' || node.type === 'JSXText') lits.push([node.loc.start.line, node.value]);
    if (node.type === 'TemplateElement') lits.push([node.loc.start.line, node.value.cooked || '']);
    for (const key of Object.keys(node)) {
      if (key === 'loc' || key === 'leadingComments' || key === 'trailingComments' || key === 'innerComments') continue;
      const v = node[key];
      if (Array.isArray(v)) v.forEach(walk); else if (v && typeof v === 'object') walk(v);
    }
  })(ast.program);
  out[file] = {literals: lits};
}
process.stdout.write(JSON.stringify(out));
"""


def main():
    files = [str(p) for p in lint.iter_source_files(lint.SRC_DIR)]
    proc = subprocess.run(
        ["node", "-e", _NODE_EXTRACTOR], input=json.dumps(files), capture_output=True, text=True, cwd=REPO_ROOT,
    )
    if proc.returncode != 0:
        print(proc.stderr)
        return 2
    babel = json.loads(proc.stdout)

    total = covered = 0
    uncovered_sample = []
    missed = []
    parse_errors = []
    for file in files:
        rel = Path(file).relative_to(REPO_ROOT).as_posix()
        entry = babel[file]
        if "error" in entry:
            parse_errors.append(f"{rel}: {entry['error']}")
            continue
        source = Path(file).read_text(encoding="utf-8", errors="replace")
        ours = {lint._normalise(text) for _, text in lint.extract_literals(source)}
        our_hits = lint.scan_text(source)
        for line, text in entry["literals"]:
            normalised = lint._normalise(text)
            if not normalised:
                continue
            total += 1
            if normalised in ours or any(normalised in o for o in ours):
                covered += 1
            elif len(uncovered_sample) < 15:
                uncovered_sample.append(f"{rel}:{line}: {normalised[:80]!r}")
            m = lint._PHRASE_RE.search(normalised)
            if m and not any(m.group(0).lower() in hit_text.lower() for _, _, hit_text in our_hits):
                missed.append(f"{rel}:{line}: babel sees {m.group(0)!r} in {normalised[:100]!r}; the lint does not")

    print(f"Files: {len(files)}  babel literals (non-empty): {total}  extracted by the lint: {covered} "
          f"({100.0 * covered / max(total, 1):.2f}%)")
    if parse_errors:
        print(f"babel parse errors ({len(parse_errors)}):", *parse_errors, sep="\n  ")
    if uncovered_sample:
        print("Sample of literals the tokeniser did not extract verbatim:", *uncovered_sample, sep="\n  ")
    if missed:
        print(f"MISSED PHRASE HITS ({len(missed)}):", *missed, sep="\n  ")
        return 1
    print("Missed phrase hits: 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
