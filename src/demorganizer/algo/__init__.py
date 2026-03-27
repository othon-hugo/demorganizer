from .propositional_logic.annihilation_law import apply_annihilation_law
from .propositional_logic.constant_folding import (
    apply_binary_constant_folding,
    apply_unary_constant_folding,
)
from .propositional_logic.double_negation import apply_double_negation
from .propositional_logic.idempotent_law import apply_idempotent_law
from .propositional_logic.identity_law import apply_identity_law
from .propositional_logic.inverse_law import apply_inverse_law

__all__ = [
    "apply_annihilation_law",
    "apply_binary_constant_folding",
    "apply_double_negation",
    "apply_idempotent_law",
    "apply_identity_law",
    "apply_inverse_law",
    "apply_unary_constant_folding",
]
