"""
Services Package

Business logic layer for the Trading Assistant application.

Services encapsulate business logic and orchestration, providing a clean
separation between HTTP handling (FastAPI) and domain logic.

Modules:
    - position_service: Position management (get, add, exit, analyze)
    - portfolio_service: Portfolio summary, snapshots, history
    - sizing_service: Position sizing calculator (POST /portfolio/size)
    - trade_service: Trade history and statistics
    - cash_service: Cash transactions and flow tracking
    - signal_service: Momentum signal generation and management
    - health_service: System health monitoring and endpoint testing
    - analytics_service: Comprehensive trading analytics and metrics
    - validation_service: Analytics calculation validation

Benefits:
    - Testable without FastAPI
    - Reusable in CLI scripts, notebooks, tests
    - Clear separation of concerns
    - Easy to mock for unit testing
"""

# Position service
from .position_service import (
    get_positions_with_prices,
    analyze_positions,
    add_position,
    exit_position,
    update_note,
    update_tags,
    mark_position_reviewed,
    get_available_tags,
    filter_by_tags,
    run_nightly_trailing_stop_update,
    run_nightly_risk_off_alerts,
)

# Portfolio service
from .portfolio_service import (
    get_portfolio_summary,
    create_daily_snapshot,
    get_performance_history
)

# Sizing service
from .sizing_service import size_position

# Trade service
from .trade_service import (
    get_trade_history_with_stats,
    get_reflection,
    save_reflection,
)

# Cash service
from .cash_service import (
    create_transaction,
    get_transaction_history,
    get_summary as get_cash_summary
)

# Signal service
from .signal_service import (
    generate_momentum_signals,
    get_signals,
    update_signal_status,
    delete_signal,
    generate_rebalance_exit_signals,
)

# Health service
from .health_service import (
    get_basic_health,
    get_detailed_health,
    get_operational_health,
    record_market_status_check,
    test_all_endpoints,
    get_db_size_info,
    send_db_size_alert_if_needed,
    record_nightly_job,
    get_scheduler_health,
)

# Analytics service
from .analytics_service import AnalyticsService

# Validation service
from .validation_service import ValidationService

from services.drawdown_service import get_drawdown_fields
from services.reports_service import get_tax_year_report, build_tax_year_pdf, build_tax_year_csv, build_monthly_pnl_csv, get_monthly_pnl_report, get_daily_pnl_report, get_arc5_compliance_summary, get_reconciliation_report
from services.grace_service import compute_grace_days_remaining

# Compliance service — ST-01 (BLG-FEAT-11, v2.3)
from services.compliance_service import get_position_compliance

__all__ = [
    # Position service
    'get_positions_with_prices',
    'analyze_positions',
    'add_position',
    'exit_position',
    'update_note',
    'update_tags',
    'mark_position_reviewed',
    'get_available_tags',
    'filter_by_tags',
    # Portfolio service
    'get_portfolio_summary',
    'create_daily_snapshot',
    'get_performance_history',
    # Sizing service
    'size_position',
    # Trade service
    'get_trade_history_with_stats',
    'get_reflection',
    'save_reflection',
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
    'get_operational_health',
    'record_market_status_check',
    'test_all_endpoints',
    'get_db_size_info',
    'send_db_size_alert_if_needed',
    'record_nightly_job',
    'get_scheduler_health',
    # Analytics service
    'AnalyticsService',
    # Validation service
    'ValidationService'
]
