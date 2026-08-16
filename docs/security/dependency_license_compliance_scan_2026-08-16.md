**Owner:** Cybersecurity & Trust Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-08-16
**Story:** ST-23 (BLG-SEC-32, EPIC-05, v8.8)

# Dependency License Compliance Scan

## 1. Purpose

First dependency-license compliance scan of this codebase — no prior scan exists. Covers `backend/requirements.txt` (via the resolved `backend/.venv`) and `package.json` (via `node_modules`), per the story's AC.

## 2. Method

- **Backend:** `pip-licenses` (installed fresh into `backend/.venv` for this scan — not a persistent dependency) against the fully resolved venv — 96 packages total (direct + transitive).
- **Frontend:** `npx license-checker --summary` / `--json` against `node_modules` — ~1,919 packages total (direct + transitive).

Both tools report the license each package's own metadata declares (`LICENSE` classifier / `package.json` `license` field), not a legal re-derivation — cross-checked manually for every non-obviously-permissive finding (below).

## 3. Findings

### 3.1 Backend (96 packages)

License distribution (permissive-dominant): 47 MIT-family, 15 Apache-family, 14 BSD-family, plus single instances of MPL-2.0, PSF-2.0, 0BSD, Zlib, CC0-1.0 — all permissive, no compliance concern.

**2 packages require closer review:**

| Package | Declared license | Assessment |
|---------|-------------------|------------|
| `frozendict` 2.4.7 | LGPLv3 | Weak copyleft. LGPL's copyleft obligation triggers on *distributing* a linked/relinked binary — this codebase is a hosted SaaS backend, never distributed as a binary or library to third parties, so the practical obligation is inapplicable. Same reasoning already applied by convention to `psycopg2-binary` below. **No action required.** |
| `psycopg2-binary` 2.9.12 | LGPL | Same reasoning as `frozendict` — hosted-service use, not distribution. Already in use as the project's sole Postgres driver (`backend/database.py`) since project inception; not a new finding, just the first time it's been formally logged against a license policy. **No action required.** |

**1 package with missing license metadata:**

| Package | Declared license | Assessment |
|---------|-------------------|------------|
| `peewee` 4.2.6 | `UNKNOWN` (empty `License` classifier in PyPI metadata) | Transitive dependency of `yfinance` (not a direct `requirements.txt` entry — confirmed via `pipdeptree --reverse --packages peewee`). Real license verified directly from the project's own repository (`github.com/coleifer/peewee/blob/master/LICENSE`): **MIT**. The empty PyPI classifier is a packaging metadata gap on `peewee`'s side, not an actual undisclosed or restrictive license. **No action required** — permissive license confirmed by direct source inspection. |

No GPL, AGPL, or other strong-copyleft license found anywhere in the backend dependency tree.

### 3.2 Frontend (~1,919 packages)

License distribution (permissive-dominant): 1,174 MIT, 74 ISC, 43 Apache-2.0, 42 CC0-1.0, 37 BSD-2-Clause, 26 BSD-3-Clause, 5 BlueOak-1.0.0, 2 Unlicense, 2 0BSD, 1 each of Python-2.0/MPL-2.0/CC-BY-4.0/BSD, plus a handful of dual-licensed packages (consumer may choose the permissive option in every case) — all permissive, no compliance concern.

**2 entries require closer review:**

| Package | Declared license | Assessment |
|---------|-------------------|------------|
| `swing-trading-model@0.1.0` | `UNLICENSED` | **This is the project's own `package.json`**, not a third-party dependency — `license-checker` includes the scanned project itself in its output. `UNLICENSED` here just means no `license` field is set in `package.json`, expected and correct for a private/internal application not published to npm. **No action required** — not a real finding. |
| `node-forge@1.4.0` | `(BSD-3-Clause OR GPL-2.0)` | Dual-licensed — the consumer may choose either license; choosing BSD-3-Clause (the permissive option) satisfies compliance without incurring any GPL obligation. **No action required.** |

No GPL-only (non-dual-licensed), AGPL, or other strong-copyleft license found anywhere in the frontend dependency tree.

## 4. Disposition

**Zero genuinely incompatible licenses found** across ~2,015 combined backend + frontend packages (direct + transitive). All findings above resolve to "no action required" on inspection — none required a fix, a replacement dependency, or an accept-risk decision with a review-by date, because none constitutes an actual incompatibility once assessed against this app's actual distribution model (hosted SaaS, never distributed as a binary or library).

This scan is a point-in-time baseline, not a recurring gate — no CI enforcement was in scope for this story (S effort, first-time scan only). A recurring cadence (e.g. alongside the existing `dependency-vuln-rescan.yml` monthly schedule) would be a reasonable follow-up if judged worthwhile — not filed as a backlog item here since it wasn't identified as a gap by this scan itself, just a possible future enhancement.

## 5. Sign-off

- [x] Backend dependency tree scanned (96 packages, full venv resolution)
- [x] Frontend dependency tree scanned (~1,919 packages, full `node_modules` resolution)
- [x] Every non-obviously-permissive finding individually assessed, not just tallied
- [x] Zero findings required a fix-or-accept-risk decision — the AC's "either fixed or has a recorded accept-risk decision" is satisfied by there being no incompatible license to fix or accept risk on
- Signed off by: PENDING — see agent-mediated review
- Date: PENDING
