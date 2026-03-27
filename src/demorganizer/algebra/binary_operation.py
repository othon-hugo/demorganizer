from __future__ import annotations

from .constant import Constant
from .expression import Expression


class BinaryOperation(Expression):
    """A boolean expression applying a binary operator to two operands."""

    def __init__(self, left: Expression | bool, op: str, right: Expression | bool):
        """Initializes the operation, wrapping bare booleans in Constants."""

        if not isinstance(left, (bool, Expression)):
            raise ValueError(f"Invalid left operand type: {type(left).__name__!r}")

        if not isinstance(right, (bool, Expression)):
            raise ValueError(f"Invalid right operand type: {type(right).__name__!r}")

        if isinstance(left, bool):
            left = Constant(left)

        if isinstance(right, bool):
            right = Constant(right)

        self.left = left
        self.op = op
        self.right = right

    def __str__(self) -> str:
        """Returns the expression as a parenthesised infix string, e.g. '(A & B)'."""

        return f"({self.left} {self.op} {self.right})"

    @property
    def variables(self) -> set[str]:
        """Returns the union of variables present in both operands."""

        return self.left.variables | self.right.variables

    def evaluate(self, bindings: dict[str, bool]) -> bool:
        """Evaluates both operands and applies the operator, raising ValueError if unknown."""

        left_val = self.left.evaluate(bindings)
        right_val = self.right.evaluate(bindings)

        match self.op:
            case self.AND:
                return left_val and right_val
            case self.OR:
                return left_val or right_val
            case self.XOR:
                return left_val ^ right_val

        raise ValueError(f"Unknown binary operator: {self.op!r}")
