"""
Formatting Utilities

Helper functions for data formatting and type conversion.
"""

from decimal import Decimal
from typing import Any, Dict, List, Union


def decimal_to_float(obj: Any) -> Union[float, Dict, List, Any]:
    """
    Recursively convert Decimal objects to float for JSON serialization.
    
    Args:
        obj: Object to convert (can be dict, list, Decimal, or any other type)
    
    Returns:
        Converted object with all Decimals replaced by floats
    
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
    return obj
