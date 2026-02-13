"""
Services Package

Business logic layer for the Trading Assistant application.

Services encapsulate business logic and orchestration, providing a clean
separation between HTTP handling (FastAPI) and domain logic.

Modules:
    - position_service: Position management (get, add, exit, analyze)
    - portfolio_service: Portfolio summary, snapshots, history
    - trade_service: Trade history and statistics
    - cash_service: Cash transactions and flow tracking
    - signal_service: Momentum signal generation and management
    - health_service: System health monitoring and endpoint testing

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

from .cash_service import (
    create_transaction,
    get_transaction_history,
    get_summary as get_cash_summary
)

from .signal_service import (
    generate_momentum_signals,
    get_signals,
    update_signal_status,
    delete_signal
)

from .health_service import (
    get_basic_health,
    get_detailed_health,
    test_all_endpoints
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
    'get_trade_history_with_stats',
    # Cash service
    'create_transaction',
    'get_transaction_history',
    'get_cash_summary',
    # Signal service
    'generate_momentum_signals',
    'get_signals',
    'update_signal_status',
    'delete_signal',
    # Health service
    'get_basic_health',
    'get_detailed_health',
    'test_all_endpoints'
]
