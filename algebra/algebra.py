from __future__ import annotations

from abc import ABC, abstractmethod


class Expression(ABC):
    def __and__(self, other: Expression) -> BinaryOperation:
        if not isinstance(other, Expression):
            return NotImplemented

        return BinaryOperation(self, "&", other)

    def __or__(self, other: Expression) -> BinaryOperation:
        if not isinstance(other, Expression):
            return NotImplemented

        return BinaryOperation(self, "|", other)

    def __xor__(self, other: Expression) -> BinaryOperation:
        if not isinstance(other, Expression):
            return NotImplemented

        return BinaryOperation(self, "^", other)

    def __invert__(self) -> UnaryOperation:
        return UnaryOperation("~", self)

    @abstractmethod
    def evaluate(self, bindings: dict[str, bool]) -> bool:
        """Evaluates the expression with a given set of variable values."""

        raise NotImplementedError

    @abstractmethod
    def __set__(self) -> set[str]:
        """Recursively finds all unique variables in the expression."""

        raise NotImplementedError


class Variable(Expression):
    def __init__(self, name: str):
        if not name.isalpha() or len(name) != 1:
            raise ValueError("variable name must be a single alphabetic character.")

        self.name = name

    def __str__(self) -> str:
        return self.name

    def __set__(self) -> set[str]:
        return {self.name}

    def evaluate(self, bindings: dict[str, bool]) -> bool:
        return bindings[self.name]


class UnaryOperation(Expression):
    def __init__(self, op: str, operand: Expression):
        self.op = op
        self.operand = operand

    def __str__(self) -> str:
        return f"({self.op}{self.operand})"

    def __set__(self) -> set[str]:
        return self.operand.__set__()

    def evaluate(self, bindings: dict[str, bool]) -> bool:
        if self.op == "~":
            return not self.operand.evaluate(bindings)

        raise ValueError(f"unknown unary operator: {self.op}")


class BinaryOperation(Expression):
    def __init__(self, left: Expression, op: str, right: Expression):
        self.left = left
        self.op = op
        self.right = right

    def __str__(self) -> str:
        return f"({self.left} {self.op} {self.right})"

    def __set__(self) -> set[str]:
        return self.left.__set__() | self.right.__set__()

    def evaluate(self, bindings: dict[str, bool]) -> bool:
        left_val = self.left.evaluate(bindings)
        right_val = self.right.evaluate(bindings)

        match self.op:
            case "&":
                return left_val and right_val
            case "|":
                return left_val or right_val
            case "^":
                return left_val ^ right_val

        raise ValueError(f"unknown binary operator: {self.op}")
