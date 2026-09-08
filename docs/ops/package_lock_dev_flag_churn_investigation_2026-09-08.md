**Owner:** Head of Engineering
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-09-08 (ST-51, EPIC-05, v9.2, BLG-TECH-12 — investigation recorded)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# `package-lock.json` `"dev": true` Churn — Root Cause Investigation

## 1. Problem

The `react-router-dom` `^7.13.0 → ^7.18.2` version bump (`3682b85b`, ST-24/BLG-TECH-11-adjacent, EPIC-05, v8.7) produced a `package-lock.json` diff far larger than the single package bump would suggest: 66 unrelated ESLint-ecosystem packages (`eslint`, `@eslint/js`, `@eslint/eslintrc`, `@eslint/config-array`, and their own transitive deps) each lost their `"dev": true` metadata flag in the same commit.

## 2. Root Cause (Confirmed Benign)

`npm`'s `"dev": true` flag on a `package-lock.json` entry means "this package is reachable *only* via `devDependencies` edges" — the moment *any* edge from a production dependency also reaches the same resolved node, npm's tree walk removes the flag, even if that edge is only a `peerDependencies` declaration.

Confirmed chain, reading the current lockfile directly:

1. `react-scripts` is listed in `package.json` **`dependencies`**, not `devDependencies` — a long-standing Create React App convention (the build tooling must be present under `npm install --production` because CRA apps are "built" as a deploy step, not run via `node` in production; see also ST-50's CRA-migration scoping doc, which inherits this same convention as a toolchain quirk rather than an app-specific choice).
2. `react-scripts` depends on `eslint-webpack-plugin`, which declares `peerDependencies: { "eslint": "^7.0.0 || ^8.0.0" }`.
3. The project's own explicit `devDependencies` pin is `"eslint": "^9.39.4"` — outside that peer range. `npm install`'s own warning output confirms the mismatch is real and unresolved: `Conflicting peer dependency: eslint@8.57.1` / `peer eslint@"^7.0.0 || ^8.0.0" from eslint-webpack-plugin@3.2.0`.
4. Despite the version mismatch, npm's peer-dependency graph still records an edge from the (production-reachable) `eslint-webpack-plugin` to the top-level `eslint` node when computing reachability for the `dev` flag — so the top-level `eslint@9.39.4` entry, and everything only *it* needs (`@eslint/js`, `@eslint/eslintrc`, `@eslint/config-array`, etc.), is now technically "reachable from a production dependency" and loses `"dev": true", regardless of whether the peer requirement is actually satisfied.
5. Confirmed directly against the current lockfile: `node_modules/eslint` itself (the explicit devDependency, not a transitive package) has no `"dev"` key at all — the flag loss reaches all the way to the root of the explicit devDependency, which is the clearest evidence this is the peer-edge mechanism above and not, say, an accidental promotion of `eslint` into `dependencies`.

A genuinely separate, unrelated nested ESLint toolchain also exists at `node_modules/eslint-config-react-app/.../eslint@8.57.1` — CRA's own bundled lint config, which correctly has no `dev` flag issue since it was never dev-only to begin with (it's wholly inside the `react-scripts` prod-dependency subtree). This is not part of the churn being investigated; noted only to avoid conflating the two ESLint installations while reading the lockfile diff.

## 3. Why This Is Benign, Not a Real Issue

- **No production bundle impact.** What ships in `build/` is controlled by webpack bundling `src/` at `npm run build` time, not by which `node_modules` entries carry a `dev` flag in the lockfile. ESLint and its `@eslint/*` packages are never imported by application source (confirmed: `grep -rn "require(['\"]eslint" src/` and equivalent import-style checks return nothing) and are not part of the CRA webpack entry graph.
- **No security-surface change.** The flag is npm-internal bookkeeping (used by `npm install --omit=dev` / `npm ci --omit=dev`) — it does not change which packages are installed by a normal `npm install`, only which subset a *production-only* install would additionally pull in.
- **Practical effect, if any:** a `npm install --omit=dev` (or `NODE_ENV=production npm ci`) run on this repo will now also install the ESLint devDependency toolchain (larger `node_modules`, marginally longer install), because npm believes it's needed for a peer that in fact isn't correctly satisfied. This repo's own CI/deploy path does not use `--omit=dev` anywhere (`.github/workflows/*.yml` and the Render build config use plain `npm install`/`npm ci`), so this has zero observed effect on any real pipeline today. Recorded here in case that changes.

## 4. Disposition

**No fix required or applied.** This is upstream `react-scripts`/`eslint-webpack-plugin`/npm peer-dependency-graph behaviour, not a defect introduced by the `react-router-dom` bump or anything specific to this repo — the bump merely triggered npm to recompute the full dependency graph's `dev` flags, surfacing pre-existing peer-mismatch bookkeeping noise that would have appeared on any lockfile-regenerating change. `eslint-webpack-plugin`'s peer range (`^7.0.0 || ^8.0.0`) not covering `eslint@9.x` is itself tracked implicitly by CRA's own toolchain-migration pressure — see `docs/ops/cra_migration_scoping_2026-09-08.md` (ST-50, same story batch), which already recommends moving off `react-scripts` rather than patching around its peer-dependency assumptions.

## 5. Sign-Off

**Head of Engineering:** Confirmed — root cause traced to the `eslint-webpack-plugin` peer-dependency edge from the production-listed `react-scripts`, verified against the current lockfile (`node_modules/eslint` itself carries no `dev` flag), confirmed no production-bundle or security impact. No fix required. 2026-09-08.

---

## Change Log

| Date | Version | Summary |
|---|---|---|
| 2026-09-08 | 1.0 | Investigation recorded (ST-51, EPIC-05, v9.2, BLG-TECH-12). |
