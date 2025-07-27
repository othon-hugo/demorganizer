from algebra import Variable
from format import create_truth_table
from morgan import (
    apply_annihilation_law,
    apply_binary_constant_folding,
    apply_double_negation,
    apply_idempotent_law,
    apply_identity_law,
    apply_inverse_law,
    apply_unary_constant_folding,
)

__all__ = [
    "Variable",
    "create_truth_table",
    "apply_annihilation_law",
    "apply_binary_constant_folding",
    "apply_double_negation",
    "apply_idempotent_law",
    "apply_identity_law",
    "apply_inverse_law",
    "apply_unary_constant_folding",
]
