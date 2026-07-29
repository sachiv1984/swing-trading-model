"""
Idempotency-key pattern for state-mutating POST endpoints (ST-03, EPIC-01,
v7.10, BLG-BE-76).

Additive, opt-in only (RISK-02): a caller that does not supply an
`idempotency_key` never touches the `idempotency_keys` table at all —
`replay_or_create()` short-circuits straight to `create_fn()` with zero extra
DB access, so existing behaviour is completely unchanged when the key is
absent.

Pattern documented in
docs/specs/api_contracts/backend_engineering_patterns.md §12.
"""
from typing import Any, Callable, Dict, Optional


def replay_or_create(
    portfolio_id: str,
    endpoint: str,
    idempotency_key: Optional[str],
    create_fn: Callable[[], Dict[str, Any]],
) -> Dict[str, Any]:
    """
    If `idempotency_key` is falsy: calls `create_fn()` and returns its result
    unchanged. No database access beyond what `create_fn()` itself performs.

    If `idempotency_key` is provided: checks for a prior record with the same
    (portfolio_id, endpoint, idempotency_key). If found, returns the cached
    response body verbatim instead of re-running `create_fn()` (dedup — no
    duplicate resource is created on a retried request). Otherwise runs
    `create_fn()`, stores the result keyed by idempotency_key, and returns it.
    """
    if not idempotency_key:
        return create_fn()

    from database import (
        ensure_idempotency_keys_table,
        get_idempotency_record,
        create_idempotency_record,
    )

    ensure_idempotency_keys_table()
    existing = get_idempotency_record(portfolio_id, endpoint, idempotency_key)
    if existing is not None:
        return existing

    result = create_fn()
    create_idempotency_record(portfolio_id, endpoint, idempotency_key, result)
    return result
