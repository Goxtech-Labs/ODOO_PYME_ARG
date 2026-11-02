"""Quantity quantum matching Odoo 20 uom.round/compare/is_zero.

Odoo 20 uses the global Product Unit precision; units no longer have a
rounding field. Currency rounding remains a separate native definition.
"""


def quantity_rounding(env):
    return 10.0 ** -env['decimal.precision'].precision_get('Product Unit')
