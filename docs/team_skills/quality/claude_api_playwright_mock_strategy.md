**Owner:** QA & Testing Owner
**Class:** Team Skills Reference (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-28
**Cycle:** 2026-05-27__release-v4.2 — ST-09 (BLG-QA-37)
**Reviewed by:** Director of Quality (agent-mediated) 2026-05-28

---

# Claude API Playwright Mock Strategy

This document defines the strategy for mocking Claude API calls in Playwright E2E tests. The goal is to prevent real Anthropic API calls during CI and local test runs while still validating the frontend behaviour of AI-powered features.

---

## 1. Why Mocking Is Required

The application calls the Anthropic API for two features:

- **AI thesis generation** — `POST /trade-plans/{plan_id}/generate-thesis` and `POST /trade-plans/generate-plan` (via `gemini_service.py`)
- **AI journal summary** — `POST /ai/journal-summary` (via `ai_service.py`)

During Playwright E2E tests:

- Real Anthropic API calls incur cost.
- CI environments do not have `ANTHROPIC_API_KEY` set.
- Network latency makes tests unreliable.
- Calling the real API in tests couples test stability to external service availability.

All Playwright tests MUST intercept Claude-backed backend endpoints and return fixture responses. No test should trigger a real Anthropic API call.

---

## 2. Intercept Architecture

Playwright mocking operates at the HTTP level via `page.route()`. The application's frontend calls the **backend** (e.g. `POST /trade-plans/generate-plan`). Playwright intercepts these backend calls from the browser.

**The mock chain for Claude-backed endpoints:**

```
Browser (React) → page.route() intercept → fixture response
                                ↕ (bypassed — no network call)
                            Backend → Claude API (never reached)
```

This is correct: Playwright tests mock the **backend API surface**, not the Anthropic SDK. The Claude API itself is never called.

---

## 3. Intercept Patterns

### 3.1 Catch-all registration rule

Follow the LIFO pattern established in `docs/team_skills/quality/playwright_patterns.md`:

```js
// Register catch-all FIRST (lowest LIFO priority)
await page.route(`${API}/`, route => route.fulfill({ status: 200, ... }));

// Register specific Claude-backed endpoint mocks AFTER (higher LIFO priority)
await page.route(`${API}/trade-plans/generate-plan`, route => { ... });
```

### 3.2 Thesis generation endpoints

```js
const API = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Mock: POST /trade-plans/generate-plan
await page.route(`${API}/trade-plans/generate-plan`, async (route) => {
  if (route.request().method() === 'POST') {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        available: true,
        fields: {
          setup_thesis: 'Mock thesis: Strong breakout above resistance.',
          entry_rationale: 'Mock rationale: ATR expanding, regime Risk On.',
          confirmation_criteria: 'Mock confirmation: Volume above average.',
          early_exit_conditions: 'Mock exit: Close below 200 SMA.',
          regime_context_at_entry: 'Risk On',
          r_target: 2.5,
        },
        model_version: 'claude-haiku-4-5',
        prompt_version: 'v3.0',
      }),
    });
  } else {
    route.continue();
  }
});

// Mock: POST /trade-plans/{plan_id}/generate-thesis
// Use a regex to match any plan_id UUID
await page.route(new RegExp(`${API}/trade-plans/[^/]+/generate-thesis`), async (route) => {
  if (route.request().method() === 'POST') {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        status: 'ok',
        data: {
          available: true,
          thesis: 'Mock thesis: Strong breakout above resistance with confirmed volume.',
          model_version: 'claude-haiku-4-5',
          prompt_version: 'v3.0',
          input_hash: 'a1b2c3d4e5f67890',
          output_hash: 'f0e9d8c7b6a54321',
        },
      }),
    });
  } else {
    route.continue();
  }
});
```

### 3.3 Journal summary endpoint

```js
// Mock: POST /ai/journal-summary
await page.route(`${API}/ai/journal-summary`, async (route) => {
  if (route.request().method() === 'POST') {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        summary: 'Mock summary: Consistent disciplined entries. Stop losses respected.',
        trade_count: 5,
        model: 'claude-haiku-4-5-20251001',
        cached: false,
        message: null,
      }),
    });
  } else {
    route.continue();
  }
});
```

### 3.4 Unavailable / degraded state

To test the frontend graceful-degradation path (when Claude API is unavailable):

```js
// Simulate Claude API unavailable
await page.route(`${API}/trade-plans/generate-plan`, async (route) => {
  route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify({
      available: false,
      error: 'ANTHROPIC_API_KEY not configured',
    }),
  });
});

// Simulate journal summary unavailable
await page.route(`${API}/ai/journal-summary`, async (route) => {
  route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify({
      summary: null,
      trade_count: 0,
      model: null,
      cached: false,
      message: 'AI summarisation is currently unavailable. Please try again later.',
    }),
  });
});
```

---

## 4. Fixture Response Format

All fixture responses must conform to the canonical contract in `docs/specs/api_contracts/`:

| Endpoint | Contract file | Key fields |
|----------|--------------|------------|
| `POST /trade-plans/generate-plan` | `ai_thesis_generation.md` v2.1.0 | `available`, `fields`, `model_version`, `prompt_version` |
| `POST /trade-plans/{plan_id}/generate-thesis` | `ai_thesis_generation.md` v2.1.0 | `status: "ok"`, `data.available`, `data.thesis`, `data.model_version` |
| `POST /ai/journal-summary` | `ai_endpoints.md` v1.2 | `summary`, `trade_count`, `model`, `cached`, `message` |

**Fixture values must be realistic but clearly fake** (e.g. prefix mock strings with `"Mock:"`) so test failures surface meaningful diffs rather than actual AI output.

---

## 5. CI Environment Guarantee

CI (`quality_gate.yml`) does not set `ANTHROPIC_API_KEY`. Any test that triggers a real Claude API call will fail silently (backend returns `available: false`) — this is the graceful degradation path, not an error. Playwright tests must assert on visible frontend behaviour, not API call presence.

To prevent accidental real calls in tests that run against a live backend (local dev with `ANTHROPIC_API_KEY` set), always register Claude-backed endpoint mocks in every test that exercises AI UI surfaces.

---

## 6. Alignment with Existing Infrastructure

This strategy aligns with the patterns in `docs/team_skills/quality/playwright_patterns.md`:

- LIFO route registration order (§1)
- API base URL via `process.env.REACT_APP_API_URL || 'http://localhost:8000'` (§2)
- `route.continue()` fallthrough for unexpected methods (§3)
- `mockBaseEndpoints()` helper pattern for shared setup (§4 of playwright_patterns.md)

Claude-backed endpoint mocks should be added to the test file's `mockBaseEndpoints()` helper or as inline mocks within individual test blocks depending on scope.

---

## 7. Director of Quality Sign-Off

**Reviewed:** Director of Quality (agent-mediated) 2026-05-28
**Decision:** APPROVED
**Notes:** Strategy correctly targets backend API surface (not Anthropic SDK), uses established LIFO pattern, provides both success and degraded-state fixture formats, and aligns with existing Playwright infrastructure. No implementation gaps identified.
