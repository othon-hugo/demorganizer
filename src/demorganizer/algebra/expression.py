from __future__ import annotations

from abc import ABC, abstractmethod


class Expression(ABC):
    """Abstract base class for all boolean expressions."""

    AND = "&"
    OR = "|"
    XOR = "^"
    NOT = "~"

    def __and__(self, other: Expression | bool) -> BinaryOperation:
        if isinstance(other, bool):
            return BinaryOperation(self, self.AND, Constant(other))

        if not isinstance(other, Expression):
            return NotImplemented

        return BinaryOperation(self, self.AND, other)

    def __or__(self, other: Expression | bool) -> BinaryOperation:
        if isinstance(other, bool):
            return BinaryOperation(self, self.OR, other)

        if not isinstance(other, Expression):
            return NotImplemented

        return BinaryOperation(self, self.OR, other)

    def __xor__(self, other: Expression | bool) -> BinaryOperation:
        if isinstance(other, bool):
            return BinaryOperation(self, self.XOR, other)

        if not isinstance(other, Expression):
            return NotImplemented

        return BinaryOperation(self, self.XOR, other)

    def __invert__(self) -> UnaryOperation:
        return UnaryOperation(self.NOT, self)

    @abstractmethod
    def evaluate(self, bindings: dict[str, bool]) -> bool:
        """Evaluates the expression with a given set of variable values."""

        raise NotImplementedError

    @property
    @abstractmethod
    def variables(self) -> set[str]:
        """Recursively finds all unique variables in the expression."""

        raise NotImplementedError


from .binary_operation import BinaryOperation  # noqa: E402
from .constant import Constant  # noqa: E402
from .unary_operation import UnaryOperation  # noqa: E402
