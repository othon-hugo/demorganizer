from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from demorganizer import algebra


def apply_annihilation_law(expr: "algebra.Expression") -> "algebra.Expression":
    """Applies Annihilation Law: A | True -> True, A & False -> False."""

    raise NotImplementedError
