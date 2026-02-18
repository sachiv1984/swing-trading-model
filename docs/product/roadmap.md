# Product Roadmap — Momentum Trading Assistant

Owner: Product Owner  
Status: Active  
Class: Planning Document (Class 4)  
Last Updated: 2026-02-18

> ⚠️ Standing Notice  
> This roadmap records product intent and sequencing only.  
> All implementation detail is indicative until confirmed in canonical specifications.  
> This document must not be treated as a source of truth for formulas, schemas, or APIs.

---

## 1. Current Version

**Current:** v1.5 — Performance Analytics  
**Next planned release:** v1.6

---

## 2. v1.6 — Position Sizing & Analytics Correctness

**Theme:** Core workflow enablement + analytics correctness  
**Rationale:**  
v1.6 delivers the Position Sizing Calculator while hardening the analytics layer so
metrics exposed to real users are mathematically correct and validation can be trusted.
These fixes are small in scope but high in impact and must not be deferred.

---

### 2.1 Position Sizing Calculator (Primary Feature)
**Status:** Planned  
**Value:** High — daily workflow improvement  

Embedded widget inside the position entry modal.  
Inputs:
- Risk percentage
- Stop distance  

Outputs:
- Optimal share count
- Real-time validation against available cash

> Before implementation:  
> The sizing formula must be canonicalised in `strategy_rules.md` by the Strategy Rules owner.

---

### 2.2 Analytics Correctness & Validation Hardening (Supporting Scope)

These items do not merit a standalone release, but **must be explicitly listed** to ensure
they are delivered as part of v1.6 and not dropped.

---

#### BLG-TECH-01 — Sharpe & Capital Efficiency Correctness (**Quality Gate**)
**Type:** Data correctness / metrics integrity  

- Fix Sharpe ratio to use sample variance (divide by n-1).
- Fix capital efficiency to use actual GBP `total_cost` from trade history.
- Update validation expected values and require canonical sign-off.

**Release Gate:**  
v1.6 **must not ship** unless this item is complete.  
This affects any user with sufficient trades to produce a non-zero Sharpe, which will
be true in real usage.

---

#### BLG-TECH-02 — Validation Severity Model
**Type:** Governance enablement  

- Add severity to each validation result.
- Add summary breakdown by severity.
- Align API responses with documented validation model.

---

#### BLG-TECH-03 — Validation Service Layer Consolidation
**Type:** Internal architecture  

- Move validation logic into service layer.
- Keep routers thin.
- Delivered alongside BLG-TECH-02 to avoid rework.

---

## 3. v1.7 — Delivery & Process Hardening

**Theme:** Engineering quality and release safety  
**Rationale:**  
This release focuses on improving delivery confidence rather than adding user-facing
capability.

---

### 3.1 CI/CD Validation Workflow
**Item:** BLG-TECH-04  
**Type:** Process improvement  

- GitHub Actions workflow running analytics validation on PRs and branch pushes.
- Block merge on critical-severity validation failures.
- Post validation summary as PR comment.

This is intentionally scheduled **after v1.6**, once severity exists and analytics
correctness has been fixed.

---

## 4. v2.0 — Deferred / Scale-Oriented Work

These items have confirmed value but are deferred until there is sufficient scale,
usage, or operational need.

- BLG-TECH-05 — Prometheus validation metrics endpoint
- Position correlation analysis
- Backtesting module
- Multi-portfolio support
- Mobile app
- Full compliance scoring system

---

## 5. Roadmap Principles

- Core workflow features take precedence over observability and automation.
- Data correctness issues are treated as release-quality gates, not optional fixes.
- Process improvements follow functional stability.
- Deferred does not mean rejected; it means intentionally sequenced.

---
