from algebra import Variable
from algo import (
    apply_annihilation_law,
    apply_binary_constant_folding,
    apply_double_negation,
    apply_idempotent_law,
    apply_identity_law,
    apply_inverse_law,
    apply_unary_constant_folding,
)
from format import create_truth_table

__all__ = [
    "apply_annihilation_law",
    "apply_binary_constant_folding",
    "apply_double_negation",
    "apply_idempotent_law",
    "apply_identity_law",
    "apply_inverse_law",
    "apply_unary_constant_folding",
    "create_truth_table",
    "Variable",
]
