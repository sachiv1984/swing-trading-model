-- BLG-BE-40 impact measurement query (ST-28, EPIC-06, v8.4)
--
-- Context: BLG-BE-40 (v6.4, commit 4d56dc42, 2026-07-02) fixed
-- signal_service.generate_momentum_signals() to source its ticker scan
-- universe from services.ticker_universe_service.get_all_tickers(active_only=True)
-- instead of the deprecated database.get_all_tickers() (`tickers` table).
--
-- The fix changes SCAN UNIVERSE MEMBERSHIP only — it does not change the
-- suggested_shares formula for a ticker that was eligible under both
-- sources. The impact is therefore signals generated for tickers that were
-- present in the deprecated `tickers` table but are NOT in the current
-- active `ticker_universe` set: those signals (and their suggested_shares
-- values) represent scans of tickers that should not have been in the
-- universe under the corrected logic.
--
-- Requires: production DATABASE_URL (this repo/CI environment has no
-- access to production data — see ESC-EXEC-20260808-05).
--
-- Run this against production Postgres (psql or any DB client):

-- Step 1 — signals generated before the fix, for tickers not in the
-- current active ticker_universe (the affected population):
SELECT
    s.id,
    s.ticker,
    s.market,
    s.signal_date,
    s.suggested_shares,
    s.allocation_gbp,
    s.status,
    s.created_at
FROM signals s
WHERE s.created_at < '2026-07-02 08:31:07'  -- commit 4d56dc42 deploy time (confirm actual deploy timestamp differs from commit timestamp if CD lag applies)
  AND NOT EXISTS (
      SELECT 1 FROM ticker_universe tu
      WHERE tu.ticker = s.ticker AND tu.active = true
  )
ORDER BY s.signal_date;

-- Step 2 — summary counts and magnitude (run after Step 1 confirms the
-- affected population; adjust the cutoff timestamp if Step 1's manual
-- review finds actual deploy time differs from the commit timestamp):
SELECT
    COUNT(*) AS affected_signal_count,
    COUNT(DISTINCT s.ticker) AS affected_ticker_count,
    SUM(s.suggested_shares) AS total_affected_suggested_shares,
    AVG(s.suggested_shares) AS avg_affected_suggested_shares,
    MIN(s.signal_date) AS earliest_affected_signal,
    MAX(s.signal_date) AS latest_affected_signal,
    SUM(s.allocation_gbp) AS total_affected_allocation_gbp
FROM signals s
WHERE s.created_at < '2026-07-02 08:31:07'
  AND NOT EXISTS (
      SELECT 1 FROM ticker_universe tu
      WHERE tu.ticker = s.ticker AND tu.active = true
  );

-- Step 3 — materiality context: what fraction of all pre-fix signals does
-- the affected population represent?
SELECT
    (SELECT COUNT(*) FROM signals WHERE created_at < '2026-07-02 08:31:07') AS total_pre_fix_signals,
    (SELECT COUNT(*) FROM signals s WHERE s.created_at < '2026-07-02 08:31:07'
        AND NOT EXISTS (SELECT 1 FROM ticker_universe tu WHERE tu.ticker = s.ticker AND tu.active = true)
    ) AS affected_pre_fix_signals;

-- Interpretation note (per this story's own AC): this is informational —
-- no remediation is implied unless a material discrepancy is found. A
-- "material discrepancy" here would mean either (a) a large fraction of
-- pre-fix signals are affected (Step 3), or (b) affected signals were
-- acted on (status IN ('entered', 'already_held') — check status column
-- in Step 1's output) rather than merely generated and dismissed/expired.
-- Signals with status='entered' among the affected population are the
-- ones with real trading impact and deserve closer individual review.
