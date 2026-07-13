"""
Formatting Utilities

Helper functions for data formatting and type conversion.
"""

from decimal import Decimal
from typing import Any, Dict, List, Union

import numpy as np


def decimal_to_float(obj: Any) -> Union[float, Dict, List, Any]:
    """
    Recursively convert Decimal and numpy scalar objects to native float/int
    for JSON serialization and DB parameter binding.

    numpy scalars (e.g. numpy.float64 from indexing a pandas Series) must be
    unwrapped before being passed to psycopg2: under numpy>=2.0, repr(np.float64(x))
    is "np.float64(x)" rather than a bare number, and psycopg2's parameter
    adapter embeds that repr as the literal SQL text — Postgres then parses
    "np.float64(...)" as a schema-qualified function call and fails with
    'schema "np" does not exist'.

    Args:
        obj: Object to convert (can be dict, list, Decimal, numpy scalar, or any other type)

    Returns:
        Converted object with all Decimals/numpy scalars replaced by native float/int

    Examples:
        >>> decimal_to_float(Decimal('123.45'))
        123.45

        >>> decimal_to_float({'price': Decimal('100.50'), 'qty': 10})
        {'price': 100.5, 'qty': 10}

        >>> decimal_to_float([Decimal('1.1'), Decimal('2.2')])
        [1.1, 2.2]
    """
    if isinstance(obj, dict):
        return {k: decimal_to_float(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [decimal_to_float(item) for item in obj]
    elif isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.integer):
        return int(obj)
    return obj
