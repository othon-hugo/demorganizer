from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from demorganizer import algebra


def apply_unary_constant_folding(expr: "algebra.Expression") -> "algebra.Expression":
    """Applies rule for negating constants: ~True -> False"""

    raise NotImplementedError


def apply_binary_constant_folding(expr: "algebra.Expression") -> "algebra.Expression":
    """Applies rule for binary operations on two constants: True & False -> False."""

    raise NotImplementedError
