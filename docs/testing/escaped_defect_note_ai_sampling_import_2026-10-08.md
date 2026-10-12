**Owner:** Director of Quality; QA & Testing Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-10-08 (ST-02, EPIC-01, v9.11, BLG-BE-150 — note filed)
**Source:** ST-02 (`BLG-BE-150`), EPIC-01, cycle `2026-10-08__release-v9.11`

---

# Escaped Defect Note — AI-Output Sampling Hook Bare Import (v9.4 to v9.10)

## What escaped

`2026-09-14__release-v9.4` ST-23 (`BLG-AI-06`, commit `75c80869`, 2026-09-15) wired the AI-output sampling hook into all six AI generation call sites (post-trade debrief, journal summary, daily briefing, chat, generate-plan, generate-thesis). Each call site imported the hook by bare module name, inside the function:

```python
from ai_output_sampling_service import maybe_sample_output
```

Production runs with `backend/` on `sys.path`, not `backend/services/`, so that import raised `ModuleNotFoundError` the first time a request reached it. The import ran only after a successful generation, inside the same `try` that returns each endpoint's generic fallback message. The effect was:

- A successful AI response was replaced by the generic "unavailable" message (briefing, chat, journal summary), or the request failed (debrief, trade-plan generation).
- The daily briefing and chat logged nothing, because their fallback handlers did not log the exception. The journal summary's handler did log it (`summarise_journal_notes failed`), but as an ordinary AI-unavailable error.
- The post-trade debrief failed only when its focus area **passed** the compliance check. A fallback debrief never reached the import, so production debriefs sometimes worked, which made the fault look intermittent.

It was first observed in production by the user on 2026-10-07 ("No module named 'ai_output_sampling_service'" on the trade history page) and fixed in PR #1921 (`08fc98c5`, merged as `d27df233`). It was live for about 22 days, across v9.4 to v9.10.

This is an **escaped defect** under `escaped_defect_and_follow_on_ratio_tracker.md`'s definition: shipped code that did not do what its own acceptance criteria required ("Never breaks the caller"), first observed after merge.

## Why ST-23's QA evidence and DoQ sign-off missed it

1. **The test environment could resolve an import that production could not.** Several test files insert `backend/services/` into `sys.path` (for example `tests/test_plan_vs_reality.py` and `tests/test_service_coverage.py`). pytest runs every file in one process, so that entry stays active for the whole run, and the bare import resolved in CI. ST-23's 29 new tests and its 31-test regression run (`qa_evidence_EPIC-05.md`, v9.4) all passed for that reason.
2. **The import was lazy.** It sat inside each function, after the model call. Importing the module, starting the app or running the smoke tests never executed it. Only a request whose model call succeeded reached it.
3. **The failure was hidden by design.** For three of the six features the import shared a `try` with the endpoint's fallback, and the briefing and chat handlers logged nothing. A broken import looked exactly like a transient AI outage, both to the user and in the logs.
4. **No live check exercised the success path.** ST-23's live-sample ACs (AC 4 and AC 6) were disclosed as staging-only and deferred (`ESC-EXEC-20260910-01`), because the session had no Anthropic key. The DoQ sign-off covered AC 1–3 and 5 by unit test and code review, and none of those runs could see the import failure (point 1).
5. **The review checked what the code said, not where it would run.** The agent-mediated sign-off reviewed the call-site wiring and found it complete. Nothing in the evidence template asks how an import resolves at runtime, so a correct-looking import line passed.

## Follow-ups

| Follow-up | What it closes | Status |
|-----------|----------------|--------|
| ST-03 (`BLG-BE-151`, v9.11) | Points 3 and 2: every call site now goes through `backend/utils/ai_sampling.py::sample_ai_output()`, which guards the import and the call and logs any failure with `exc_info`. The daily briefing and chat log the exception behind their fallback message. `tests/test_ai_sampling_failsafe.py` asserts each of the six endpoints returns the same response when sampling fails at import or inside the hook. | Done (`6151c0c0`) |
| ST-04 (`BLG-QA-217`, v9.11) | Points 1 and 2: `tests/test_backend_import_path_isolation.py` runs in a clean subprocess with only `backend/` on `sys.path`. It imports every backend module and resolves every import statement, including function-level ones. Reintroducing the bare import fails it. It runs in CI Phase A. | Done (`7e4ebd11`) |
| `BLG-QA-218` | Point 1 at its source: stop test files adding `backend/services/` to `sys.path`, with a guard. | Open (backlog, P3) |
| PR #1921 static guard | `tests/test_backend_service_import_paths.py` fails on a bare import of a `backend/services` module. | Done (2026-10-07) |
| ST-02 (`BLG-BE-150`, v9.11) | Point 4: a dated staging run of all six AI features after the fix, and a recorded sampling check. | Delegated (`DEL-20261008-01`) |

## Lesson for QA evidence

A story that adds a call into code reached only on a live success path (a lazy import, a post-success hook, a fallback-guarded branch) needs either a test that runs under production's import path, or a live run of that success path, before DoQ sign-off. Unit tests in a shared pytest process do not show how an import resolves in production. ST-04's test now covers the import-path half for every future story.
