**Owner:** Cybersecurity & Trust Lead
**Class:** Operational Policy (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-08-08
**Cycle:** 2026-08-07__release-v8.4 (ST-18 — BLG-SEC-12, RISK-02)

---

# CSP `'unsafe-inline'` Removal Audit — script-src / style-src

## Purpose

ST-18 (BLG-SEC-12, RISK-02 Medium): the CSP in `public/index.html` carried a blanket `'unsafe-inline'` for both `script-src` and `style-src`, materially weakening the policy's protection against injected/reflected script execution. Audit every genuine inline-script and inline-style source in the app, remove the blanket exception where a narrower alternative exists, and confirm no functional regression under the tightened policy.

## Method

Full-repo scan for: `<script>` tags in `public/index.html`; `dangerouslySetInnerHTML` usage in `src/` (the only React mechanism that can inject raw HTML, including inline `<style>`/`<script>` content, bypassing JSX's normal escaping); `eval(`/`new Function(` (dynamic code execution requiring `'unsafe-eval'`, a separate directive not in scope here but checked for completeness). Findings were then verified empirically — not just by static reading — using a real headless Chromium (`/usr/bin/chromium-browser`) loading the app under the tightened CSP via Playwright, capturing all `Content-Security-Policy` console violation reports across five representative pages (Dashboard, Reports, Positions, Watchlist, TradeReflection) and the full existing Playwright regression suite for the app areas touched.

## Findings

**Two inline-content sources found — one for script-src, one for style-src. No `eval`/`new Function` found.**

| # | Location | Content | script-src or style-src | Static or dynamic |
|---|----------|---------|--------------------------|--------------------|
| 1 | `public/index.html` — single `<script type="text/javascript">` block | The `spa-github-pages` redirect trick (rewrites a `?/encoded-path` query string back into a real path via `history.replaceState`) — required because this app deploys to GitHub Pages, which has no server-side rewrite for client-side routes on a hard refresh/deep link | script-src | **Static** — fixed content, never varies |
| 2 | `src/components/ui/chart.js`'s `ChartStyle` — a `<style dangerouslySetInnerHTML>` | Generates `[data-chart=<id>] { --color-<key>: <value>; }` (and a `.dark [data-chart=<id>] { ... }` variant) from the `ChartContainer`'s `config` prop, so each chart instance's Recharts colour palette is theme-reactive via pure CSS cascade, no JS re-render needed on theme toggle | style-src | **Dynamic** — content depends on the `config` prop passed to each chart instance; note this primitive currently has no call sites in the app (`src/components/ui/chart.js` is unused shadcn/ui boilerplate) but is retained as ready-to-use shared UI infrastructure |

## Disposition

**script-src: `'unsafe-inline'` removed entirely, replaced with a content hash.** Finding #1's content is static, so `'sha256-5Oi72KUZ3LaSR2N9JWbDZVUqXP38QIpVD1g9wfJx/HA='` (computed from the exact inline script text, confirmed via a real Chromium CSP violation report rather than an offline hash computation — see Verification below) authorises exactly that one script and nothing else. Any future inline `<script>` added to `index.html`, or any injected/reflected script from an XSS vector, is blocked outright; this is a strictly stronger policy than the blanket exception it replaces.

**style-src: `'unsafe-inline'` retained, narrowly justified.** Finding #2's content is dynamic (varies per chart config and current theme), so neither a static hash nor a per-request nonce (this is a static SPA build with no server-side templating to inject a nonce at request time) is viable. Per this story's own AC ("style-src narrowed or justified explicitly if any exception remains"), the exception is kept and documented inline in `public/index.html` alongside the CSP meta tag, and here. Removing it entirely would require either (a) reworking `ChartStyle` to set CSS custom properties via inline `style` attributes on `ChartContainer` directly — which is not restricted by CSP's `style-src` since React sets inline styles via the CSSOM (`element.style.property = value`), not via the `style=""` HTML attribute or an actual `<style>` element — losing the theme-conditional (`.dark` selector) value switching in the process, since inline `style` values are static per render and would need explicit theme-change reactivity added; or (b) removing the primitive. Given `chart.js` has zero current call sites, this rework carries real implementation and testing risk for a component nobody currently uses, with no live behavioural benefit today — deferred rather than done speculatively. Filed as `BLG-FE-146` for future consideration if/when a consumer adopts `ChartContainer`.

## Verification

Playwright + a real headless Chromium (`/usr/bin/chromium-browser`, this environment's Playwright-bundled Chromium is not installable on its host OS — see `docs/ops/keyboard_navigation_audit_2026-07-29.md` for the same constraint) loaded the app under the tightened CSP and captured browser console CSP violation reports:

- Five representative pages (Dashboard, Reports, Positions, Watchlist, TradeReflection) loaded with **zero** `script-src`/`style-src` violations.
- The existing Playwright regression suite for the touched/adjacent areas (`watchlist.spec.js`, `dialog-classname-override-fixes.spec.js`, `reports-performance-tab.spec.js`, `smoke-critical-paths.spec.js`) re-run against the tightened CSP — see `qa_evidence_EPIC-04.md` for the pass/fail record.
- The SPA-redirect inline script's exact hash was taken directly from the browser's own CSP violation report (`Refused to execute inline script ... a hash ('sha256-...') ... is required`) rather than trusted from an offline computation — the first computed hash (via a Python regex extraction of the script body) was subtly wrong (whitespace mismatch against the browser's actual parsed text-node content) and would have silently broken the GitHub Pages deep-link redirect in production had it not been checked against a real browser's own report.

**Unrelated, pre-existing finding (out of scope):** `connect-src 'self' https:` blocks `http://localhost:8000` API calls in local dev (this app's dev-mode default backend URL is plain `http://`, not `https://`). This directive was not touched by this story and is unaffected by the script-src/style-src changes — verified via `git diff` showing zero change to the `connect-src` value. Production/staging backends are `https://`, so this does not affect any real deployment; no action taken.

## Sign-off

**Cybersecurity & Trust Lead:** Confirmed — 2026-08-08
