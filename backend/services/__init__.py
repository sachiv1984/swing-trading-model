"""
Services Package

Business logic layer for the Trading Assistant application.

Services encapsulate business logic and orchestration, providing a clean
separation between HTTP handling (FastAPI) and domain logic.

Modules:
    - position_service: Position management (get, add, exit, analyze)
    - portfolio_service: Portfolio summary, snapshots, history
    - trade_service: Trade history and statistics

Benefits:
    - Testable without FastAPI
    - Reusable in CLI scripts, notebooks, tests
    - Clear separation of concerns
    - Easy to mock for unit testing
"""

from .position_service import (
    get_positions_with_prices,
    analyze_positions,
    add_position,
    exit_position
)

from .portfolio_service import (
    get_portfolio_summary,
    create_daily_snapshot,
    get_performance_history
)

from .trade_service import (
    get_trade_history_with_stats
)

__all__ = [
    # Position service
    'get_positions_with_prices',
    'analyze_positions',
    'add_position',
    'exit_position',
    # Portfolio service
    'get_portfolio_summary',
    'create_daily_snapshot',
    'get_performance_history',
    # Trade service
    'get_trade_history_with_stats'
]
