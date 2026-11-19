Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-11-19

# Execution Escalations — 2026-11-18__release-v9.18

## ESC-EXEC-20261119-01

- **Raised at:** 2026-11-19T08:07:49Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-11-18__release-v9.18
- **Step:** STEP 3.1.D (EPIC-01; ST-05 is `delegated_decision` at seal, "raise at sprint start")
- **ST/EPIC item:** ST-05 / EPIC-01 (BLG-SEC-46)
- **Trigger type:** Lifecycle
- **Blocking statement:** ST-05 needs a dated re-review decision by the Cybersecurity & Trust Lead and the Product Owner on the 2026-10-15 open-access accept-risk (`docs/operations/credential_policy.md` §1.1), explicitly covering **read** access to the owner's real positions, cash, P&L and journal. Facts for the review: the front end has no sign-in (`AuthContext.js` hard-codes one user); the site URL is public and named in `package.json`; the repository is public; there is no `robots.txt` or `noindex` under `public/`; `REACT_APP_API_KEY` is in the public bundle and authorises all routes, reads and writes; the public source map (BLG-OPS-221) makes the bundle easier to read. Options: **(1)** keep the acceptance with reasons, and add `noindex` + `robots.txt` (filed as its own item); **(2)** put access control in front of the static site (for example a Cloudflare Access / basic-auth proxy), filed as a v9.20 remedy item; **(3)** narrow the front-end key (the earlier option (a): read-only or allowlisted key), filed as its own item; **(4)** another remedy.
- **Engine recommendation (non-binding):** (2) as the v9.20 remedy, with (1)'s `noindex`/`robots.txt` filed now as a small interim item. Read exposure of real financial data is not reduced by (3), because a read-only key still exposes every read; only access control in front of the site (and the API) closes it.
- **Owning authority:** Cybersecurity & Trust Lead; Product Owner
- **Unblock criteria:** a dated decision from both owners, recorded in `credential_policy.md` §1.1 (with review triggers updated), covering read access; any remedy filed as its own backlog item.
- **SLA due-by:** 2026-11-20T08:07:49Z (24h — Lifecycle)
- **Blocks execution:** No
- **Disposition:** Open
