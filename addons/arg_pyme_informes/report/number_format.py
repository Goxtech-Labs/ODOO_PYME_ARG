from decimal import Decimal
from odoo.tools.float_utils import float_round


def decimal_digits(rounding):
    return max(0, -Decimal(str(rounding)).normalize().as_tuple().exponent)


def numeric_value(value, rounding=None, digits=None):
    """Format after aggregation; money uses its rounding, quantities their decimal field precision."""
    if digits is None:
        digits = decimal_digits(rounding)
        rounded = float_round(value, precision_rounding=rounding, rounding_method='HALF-UP')
    else:
        # A UoM step is not a constraint on already recorded commercial quantities.
        rounded = float_round(value, precision_digits=digits, rounding_method='HALF-UP')
    return rounded, digits, format(rounded, f'.{digits}f')
