#!/usr/bin/env bash
# ST-20 (BLG-OPS-133, EPIC-05, v8.4) — live latency measurement for endpoints
# missing from docs/ops/api_performance_baseline.md.
#
# Re-derived against the corrected openapi.yaml (post-BLG-SPEC-116 fix, per
# ST-20's own dependency on ST-02) yields 16 genuinely missing endpoints, not
# the original 19 named in BLG-OPS-133 (5 were already resolved/incorrect;
# 2 newly-visible ones — DELETE /watchlist/{id}, GET /news/{id} — were
# trapped inside `components:` under the old parse and are now visible).
#
# Of those 16, only the 7 below are safe to fire live: pure GET reads, all
# already used verbatim by backend/routers/test.py's own smoke-test harness
# (the exact same calls production already makes on every POST /test/endpoints
# run). The remaining 9 are excluded here because they mutate real state:
#   - GET /positions/analyze mutates trailing stops DESPITE the GET verb
#     (see backend/routers/test.py's own exclusion comment)
#   - DELETE /watchlist/{id}, PATCH /watchlist/{id}, POST /alerts/rules,
#     POST /settings are write ops per the same exclusion list
#   - POST /positions/nightly-stop-update, POST /positions/risk-off-alerts,
#     POST /positions/{id}/refresh-state, POST /signals/rebalance-exit all
#     confirmed by reading their handler code: each writes to the DB
#     (recomputes/stores trailing stops, flags positions, refreshes
#     lifecycle state, or generates new signals)
# These 9 should be added to api_performance_baseline.md §2.2 ("Endpoints
# Not Measured") rather than measured — see the write-up template at the
# bottom of this file's companion note.
#
# Usage:
#   STAGING_API_KEY=<your key> ./st20_endpoint_latency_measurement.sh
#
# Prints a JSON block (RESULTS_JSON_START / RESULTS_JSON_END) — paste that
# back and it'll be turned into the api_performance_baseline.md rows.

set -euo pipefail

: "${STAGING_API_KEY:?Set STAGING_API_KEY before running (same value as the STAGING_API_KEY GitHub secret)}"
STAGING_API_URL="${STAGING_API_URL:-https://trading-assistant-api-staging.onrender.com}"

echo "Warming service..." >&2
curl -s -o /dev/null --max-time 30 "${STAGING_API_URL}/health" || true

declare -A ENDPOINTS=(
  ["GET /analytics/market-correlation"]="/analytics/market-correlation"
  ["GET /analytics/metrics"]="/analytics/metrics?period=all_time"
  ["GET /analytics/tag-performance"]="/analytics/tag-performance?tags=momentum"
  ["GET /news/{id}"]="/news/AAPL"
  ["GET /positions/grace-period-alerts"]="/positions/grace-period-alerts"
  ["GET /positions/tags"]="/positions/tags"
  ["GET /positions/{id}/stop-trail"]="/positions/00000000-0000-0000-0000-000000000000/stop-trail"
)

echo "RESULTS_JSON_START"
echo "{"
first=true
for name in "${!ENDPOINTS[@]}"; do
  path="${ENDPOINTS[$name]}"
  times=()
  status=""
  for i in 1 2 3 4 5 6 7; do
    result=$(curl -s -o /dev/null --max-time 30 \
      -H "X-API-Key: ${STAGING_API_KEY}" \
      -w "%{time_total} %{http_code}" \
      "${STAGING_API_URL}${path}")
    t=$(echo "$result" | awk '{print $1}')
    status=$(echo "$result" | awk '{print $2}')
    times+=("$t")
  done
  sorted=($(printf '%s\n' "${times[@]}" | sort -n))
  n=${#sorted[@]}
  p50_idx=$(( (n * 50 + 99) / 100 - 1 ))
  p95_idx=$(( (n * 95 + 99) / 100 - 1 ))
  [ $p50_idx -lt 0 ] && p50_idx=0
  [ $p95_idx -ge $n ] && p95_idx=$((n - 1))
  p50=$(awk "BEGIN{printf \"%.0f\", ${sorted[$p50_idx]} * 1000}")
  p95=$(awk "BEGIN{printf \"%.0f\", ${sorted[$p95_idx]} * 1000}")
  max=$(awk "BEGIN{printf \"%.0f\", ${sorted[$((n-1))]} * 1000}")
  if [ "$first" = true ]; then first=false; else echo ","; fi
  echo -n "  \"${name}\": {\"path\": \"${path}\", \"p50_ms\": ${p50}, \"p95_ms\": ${p95}, \"max_ms\": ${max}, \"http\": ${status}, \"samples\": ${n}}"
done
echo ""
echo "}"
echo "RESULTS_JSON_END"
