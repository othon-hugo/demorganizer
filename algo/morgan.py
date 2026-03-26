from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from algebra import Expression


def apply_double_negation(expr: "Expression") -> "Expression":
    """Applies Double Negation theorem: ~(~A) -> A"""

    raise NotImplementedError


def apply_unary_constant_folding(expr: "Expression") -> "Expression":
    """Applies rule for negating constants: ~True -> False"""

    raise NotImplementedError


def apply_binary_constant_folding(expr: "Expression") -> "Expression":
    """Applies rule for binary operations on two constants: True & False -> False."""

    raise NotImplementedError


def apply_idempotent_law(expr: "Expression") -> "Expression":
    """Applies Idempotent Law: A | A -> A, A & A -> A."""

    raise NotImplementedError


def apply_inverse_law(expr: "Expression") -> "Expression":
    """Applies Inverse Law: A | ~A -> True, A & ~A -> False."""

    raise NotImplementedError


def apply_annihilation_law(expr: "Expression") -> "Expression":
    """Applies Annihilation Law: A | True -> True, A & False -> False."""

    raise NotImplementedError


def apply_identity_law(expr: "Expression") -> "Expression":
    """Applies Identity Law: A | False -> A, A & True -> A."""

    raise NotImplementedError
