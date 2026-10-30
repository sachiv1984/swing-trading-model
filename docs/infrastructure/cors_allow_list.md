**Owner:** Cybersecurity & Trust Lead; Infrastructure & Operations Owner
**Class:** Reference Document (Class 3)
**Status:** Active
**Last Updated:** 2026-10-30 (BLG-SEC-44 — deployed staging and production preflight checks recorded; staging defaults confirmed); prior — 2026-10-30 (ST-43, BLG-SEC-43, EPIC-06, v9.14 — created: per-environment CORS allow-list, defaults and precedence); prior history retained — see prior entries in version control
**Cycle:** 2026-10-29__release-v9.14 (ST-43)

---

# Per-Environment CORS Allow-List

The API's CORS allow-list is chosen per deployment. Until v9.14, `backend/config.py` held one `ALLOWED_ORIGINS` list for every environment. Production therefore accepted credentialed cross-origin requests (`allow_credentials=True`, `allow_methods=["*"]`) from `http://localhost:3000` and the staging frontend (BLG-SEC-43).

## How the list is chosen

`backend/config.py` resolves `ALLOWED_ORIGINS` once, at startup, and `backend/main.py` passes it to `CORSMiddleware`. The first rule that applies wins:

1. **`CORS_ALLOWED_ORIGINS`**: a comma-separated list of origins. If it is set and not blank, it replaces the defaults completely. Spaces and a trailing `/` are removed from each entry.
2. **`DEPLOY_ENV`**: `production`, `staging` or `development` (case-insensitive) selects that environment's default list. Any other value stops the API at startup with a `ValueError`, so a typo is seen at deploy time instead of silently picking a list.
3. **Render inference**: Render sets `RENDER` and `RENDER_SERVICE_NAME` on every service. A service whose name ends in `-staging` is `staging`; any other Render service, including a preview, is `production`, the strictest list.
4. **Off Render**: with no `RENDER` variable (local `uvicorn`, CI), the environment is `development`.

## Default lists

| Environment | Origins |
|-------------|---------|
| `production` | `https://sachiv1984.github.io` (GitHub Pages frontend); `https://trading-assistant-api-c0f9.onrender.com` (the API's own origin) |
| `staging` | `https://trading-assistant-staging.onrender.com` (staging frontend, `render.yaml`); `http://localhost:3000` (a local frontend pointed at staging) |
| `development` | `http://localhost:3000`; `http://127.0.0.1:3000` |

Production no longer accepts `http://localhost:3000` or the staging frontend. The defaults are `CORS_DEFAULT_ORIGINS` in `backend/config.py`. Change them there and in this table together.

## Per-service settings

| Service | Setting | Resulting list |
|---------|---------|----------------|
| `trading-assistant-api-staging` (`render.yaml`) | `DEPLOY_ENV=staging` in `render.yaml`. Render inference gives the same result if the Blueprint has not synced it. | `staging` |
| Production API (Render dashboard, not in `render.yaml`) | Set `DEPLOY_ENV=production` in the Render dashboard. Until it is set, inference already resolves `production` from the service name. | `production` |

Use `CORS_ALLOWED_ORIGINS` only when a deployment needs a list that is not one of the defaults (for example, a renamed staging frontend).

## Verifying a deployment

A preflight from an allowed origin returns `200` with `access-control-allow-origin` set to that origin. One from any other origin returns `400` (`Disallowed CORS origin`) with no `access-control-allow-origin` header:

```bash
curl -s -o /dev/null -w '%{http_code}\n' -X OPTIONS "$API_URL/positions" \
  -H 'Origin: http://localhost:3000' -H 'Access-Control-Request-Method: GET'   # production: 400
curl -s -D - -o /dev/null -X OPTIONS "$API_URL/positions" \
  -H 'Origin: https://sachiv1984.github.io' -H 'Access-Control-Request-Method: GET' \
  | grep -i '^access-control-allow-origin'                                       # production: the Pages origin
```

`OPTIONS` requests are exempt from the API key check (`backend/main.py` `api_key_middleware`), so these need no key. `tests/test_cors_allow_list.py` checks the production result in CI. The checks on the deployed staging and production services are recorded under BLG-SEC-44.

## Deployed checks

Recorded for BLG-SEC-44 after PR #2133 merged (merge commit `5e7351af`, live on production per the user). Each cell is one `OPTIONS /positions` preflight with `Access-Control-Request-Method: GET`, sent with the loop below, showing the status code and the `access-control-allow-origin` header.

```bash
for API_URL in https://trading-assistant-api-c0f9.onrender.com https://trading-assistant-api-staging.onrender.com; do
  for ORIGIN in http://localhost:3000 https://sachiv1984.github.io https://trading-assistant-staging.onrender.com; do
    curl -s -m 90 -D - -o /dev/null -X OPTIONS "$API_URL/positions" \
      -H "Origin: $ORIGIN" -H 'Access-Control-Request-Method: GET'
  done
done
```

| Run (2026-10-30, UTC) | Production `DEPLOY_ENV` | API | `http://localhost:3000` | `https://sachiv1984.github.io` | `https://trading-assistant-staging.onrender.com` |
|---|---|---|---|---|---|
| 15:18:02–15:19:50Z | not set (Render inference) | Production (`trading-assistant-api-c0f9`) | `400`, no allow-origin | `200`, allow-origin `https://sachiv1984.github.io` | `400`, no allow-origin |
| 15:18:02–15:19:50Z | — | Staging (`trading-assistant-api-staging`, `DEPLOY_ENV=staging`) | `200`, allow-origin `http://localhost:3000` (retried: the first request timed out while the service woke) | `400`, no allow-origin | `200`, allow-origin `https://trading-assistant-staging.onrender.com` |
| 15:29:12Z | `production` (set by the user in the Render dashboard) | Production | `400`, no allow-origin | `200`, allow-origin `https://sachiv1984.github.io` | `400`, no allow-origin |
| 15:29:12Z | — | Staging | `200`, allow-origin `http://localhost:3000` | `400`, no allow-origin | `200`, allow-origin `https://trading-assistant-staging.onrender.com` |

Every result matches the default lists above, both before and after `DEPLOY_ENV=production` was set. The production API answering after the change shows it started with the new value. The same session sent `GET /zz-auth-probe-nonexistent` with no `X-API-Key` to both APIs: both returned `401`, so the API key, not CORS, is the access control on both.

**Staging defaults confirmed (2026-10-30):** agent-mediated review on behalf of the Cybersecurity & Trust Lead (`execution_prompt.md` §5.3), accepted by the user. Staging keeps credentialed `http://localhost:3000` and the staging frontend, and rejects the Pages origin. CORS only limits which browser pages can read responses. Both APIs enforce `X-API-Key`, and staging holds only staging data. Rejecting the Pages origin stops the production frontend from being pointed at staging. Follow-up: `allow_credentials=True` in `backend/main.py` is not needed, because the frontend authenticates with a header and sends no cookies (BLG-SEC-45).
