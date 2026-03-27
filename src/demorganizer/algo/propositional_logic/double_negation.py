from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from demorganizer import algebra


def apply_double_negation(expr: "algebra.Expression") -> "algebra.Expression":
    """Applies Double Negation theorem: ~(~A) -> A"""

    raise NotImplementedError
