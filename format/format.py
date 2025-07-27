from itertools import product
from typing import TYPE_CHECKING

from tabulate import tabulate

if TYPE_CHECKING:
    from algebra.algebra import Expression


def create_truth_table(expression: "Expression") -> str:
    """Generates the truth table for the entire expression."""

    variables = sorted(list(expression.__set__()))

    # Generate all possible combinations for the variables
    combinations = [*product([True, False], repeat=len(variables))]

    headers = variables + [str(expression)]
    values: list[list[int]] = []

    for combo in combinations:
        # Create a mapping from variable names to their current boolean values
        bindings = dict(zip(variables, combo))

        # Evaluate the expression with the current values
        result = expression.evaluate(bindings)
        values += [[*map(int, combo)] + [int(result)]]

    return tabulate(values, headers, numalign="center")
