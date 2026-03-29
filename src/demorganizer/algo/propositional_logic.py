from demorganizer.engine import BooleanExpression


def apply_annihilation_law(expr: "BooleanExpression") -> "BooleanExpression":
    """Applies Annihilation Law: A | True -> True, A & False -> False."""

    raise NotImplementedError


def apply_unary_constant_folding(expr: "BooleanExpression") -> "BooleanExpression":
    """Applies rule for negating constants: ~True -> False"""

    raise NotImplementedError


def apply_binary_constant_folding(expr: "BooleanExpression") -> "BooleanExpression":
    """Applies rule for binary operations on two constants: True & False -> False."""

    raise NotImplementedError


def apply_double_negation(expr: "BooleanExpression") -> "BooleanExpression":
    """Applies Double Negation theorem: ~(~A) -> A"""

    raise NotImplementedError


def apply_idempotent_law(expr: "BooleanExpression") -> "BooleanExpression":
    """Applies Idempotent Law: A | A -> A, A & A -> A."""

    raise NotImplementedError


def apply_identity_law(expr: "BooleanExpression") -> "BooleanExpression":
    """Applies Identity Law: A | False -> A, A & True -> A."""

    raise NotImplementedError


def apply_inverse_law(expr: "BooleanExpression") -> "BooleanExpression":
    """Applies Inverse Law: A | ~A -> True, A & ~A -> False."""

    raise NotImplementedError
