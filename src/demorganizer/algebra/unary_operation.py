from __future__ import annotations

from .constant import Constant
from .expression import Expression


class UnaryOperation(Expression):
    """A boolean expression applying a unary operator to a single operand."""

    def __init__(self, op: str, operand: Expression | bool):
        """Initializes the operation, wrapping bare booleans in a Constant."""
        if not isinstance(operand, (bool, Expression)):
            raise ValueError(f"Invalid operand type: {type(operand).__name__!r}")

        if isinstance(operand, bool):
            operand = Constant(operand)

        self.operand = operand
        self.op = op

    def __str__(self) -> str:
        """Returns the expression as a parenthesised string, e.g. '(~A)'."""
        return f"({self.op}{self.operand})"

    @property
    def variables(self) -> set[str]:
        """Returns the set of variables present in the operand."""
        return self.operand.variables

    def evaluate(self, bindings: dict[str, bool]) -> bool:
        """Evaluates the unary operation, raising ValueError for unknown operators."""
        if self.op == "~":
            return not self.operand.evaluate(bindings)

        raise ValueError(f"Unknown unary operator: {self.op!r}")
