**Owner:** Head of UX & Design
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-10-08 (ST-27, EPIC-04, v9.11, BLG-FE-84 — initial version)
**Source:** ST-27 (`BLG-FE-84`), EPIC-04, cycle `2026-10-08__release-v9.11`

---

# AI Chat Advisor — Interaction Study Protocol

## 1. Purpose

The AI chat advisor (`POST /ai/chat`, `AiChatWidget.js`) shipped in v6.2. The 2026-09-24 usage review found 10 chat questions on 3 days in 102 days, the last on 2026-08-17. The audit log says how often the chat is used. It cannot say why it is used so rarely, what the user asks it, or whether the answers help. This protocol sets out a short, repeatable study to answer five questions about that.

This document defines the study. It does not run it (ST-27 scope: protocol only). The gate on running it (the AI adoption window) was removed by Product Owner decision on 2026-10-05.

## 2. Participant and Setting

- **Participant:** the product's single user (the trader). This is a single-user product, so the study is a structured self-study with a facilitator, not a panel.
- **Facilitator:** Head of UX & Design, or the Product Owner acting for the role. The facilitator observes and records but never answers on the advisor's behalf.
- **Environment:** production, with the user's real portfolio. The chat is read-only and advisory (§13, SRB-v1.7), so the study creates no trading risk.
- **§13 guard:** the facilitator must not ask the user to act on an answer, and must not suggest trades. The study observes decision-support use only. If the user decides to trade during a session, the facilitator notes it and stays out of the decision.

## 3. Study Questions

| # | Question | Why it matters |
|---|----------|----------------|
| Q1 | **When does the user think of asking the chat, and what do they do instead when they don't?** | Usage is very low. This finds whether the chat is forgotten, hard to reach, or not needed. |
| Q2 | **What does the user ask?** (portfolio state, a specific position or stop, a signal, strategy rules, or something outside scope) | Shows whether real questions match what the chat has context for (positions, stops, signals, and from v9.11 stop recalculation times). |
| Q3 | **Does the answer help the decision in front of the user?** (used, checked against another screen, ignored, or misleading) | The basis for the Response Acceptance Rate (`metrics_definitions.md` § AI Chat Engagement), which has no data until a rating control ships (`BLG-FE-208`). |
| Q4 | **Does the user trust the numbers in the answer, and do they check them?** | The chat states prices, stops and P&L. Unverified trust is a §13 risk; habitual re-checking means the answer adds little. |
| Q5 | **What would make the user come back to the chat?** (a different entry point, proactive placement, better answers, nothing) | Turns findings into candidate backlog items. |

## 4. Method

Three parts, over about two weeks of normal use. Each part maps to the questions it answers.

### 4.1 Usage diary (Q1, Q2) — 10 trading days

After each trading session the user records, in one or two lines:
- whether they opened the chat, and why or why not;
- each question asked (verbatim, or paraphrased if it named a sensitive detail);
- where they looked for the answer if they did not use the chat.

### 4.2 Observed sessions (Q2, Q3, Q4) — 3 sessions of about 20 minutes

The facilitator watches the user do their normal routine (Dashboard → Positions → Signals), thinking aloud. When the user would naturally have a question, the facilitator asks: "Would you ask the chat that?" If yes, the user asks it. For each answer the facilitator records:
- whether the answer addressed the question;
- whether the user used it, checked it against another screen, or ignored it;
- any number the user checked, and whether it matched;
- any wording that read as an instruction rather than advice (a §13 signal: report it to the Strategy Rules & System Intent Owner the same day).

### 4.3 Closing interview (Q1, Q5) — 15 minutes

Five fixed prompts, one per study question:
1. "Walk me through the last time you had a question about your portfolio. Where did you look first?"
2. "Which question would you most like the chat to answer well?"
3. "Think of an answer from this week. Did it change what you did or looked at?"
4. "When the chat gives a number, what do you do with it?"
5. "What would have to change for you to use the chat every week?"

## 5. Data Captured

| Source | What | Used for |
|--------|------|----------|
| Usage diary | Opened / not opened, reason, questions, alternative source | Q1, Q2 |
| Session notes | Question, answer fit, use / check / ignore, numbers checked, §13 wording flags | Q2, Q3, Q4 |
| `claude_audit_log` (`POST /ai/chat` rows, study window) | Call times and counts; the chat engagement measures (sessions per week, questions per session) | Cross-check against the diary; Q1 |
| Closing interview notes | Answers to the five prompts | Q1, Q5 |

No answer text is copied into the study record beyond short quotes needed to explain a finding. Full chat responses are not stored by the system (`docs/ops/claude_api_log_hygiene_policy.md`), and the study does not change that.

## 6. Analysis and Outputs

- A short findings record, `docs/product/decisions/decisions--<cycle>--ai-chat-interaction-study-findings.md`, with one section per study question, the evidence for it, and a confidence level (low, medium, high).
- For each finding that calls for a change: a new backlog item filed through `/backlog-add`, with the study as its `Source`.
- A one-paragraph input to the 2027-01-03 AI feature usage review (`BLG-GOV-382`), so engagement data and the reasons behind it are read together.
- Any §13 wording flag is handled immediately, not held for the findings record.

## 7. Timing

Run the study in the 4 weeks before the 2027-01-03 review, so its findings and the review's audit-log data cover the same period. If the monthly P&L narrative (ST-25) has shipped by then, add one observed session of that feature using the same §4.2 method.

## 8. Sign-off

- Head of UX & Design: protocol defined at ST-27 (v9.11). Run and findings pending.
