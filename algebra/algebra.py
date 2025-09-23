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


class Constant(Expression):
    def __init__(self, value: bool):
        self.value = value

    def __str__(self) -> str:
        return {True: "1", False: "0"}[self.value]

    @property
    def variables(self) -> set[str]:
        return set()

    def evaluate(self, bindings: dict[str, bool]) -> bool:
        return self.value


class Variable(Expression):
    def __init__(self, name: str):
        if not name.isalpha() or len(name) != 1:
            raise ValueError("variable name must be a single alphabetic character.")

        self.name = name

    def __str__(self) -> str:
        return self.name

    @property
    def variables(self) -> set[str]:
        return {self.name}

    def evaluate(self, bindings: dict[str, bool]) -> bool:
        if self.name not in bindings:
            raise ValueError(f"Missing binding for variable: {self.name!r}")

        return bindings[self.name]


class UnaryOperation(Expression):
    def __init__(self, op: str, operand: Expression | bool):
        if not isinstance(operand, (bool, Expression)):
            raise ValueError(f"invalid operand type: {type(operand).__name__!r}")

        if isinstance(operand, bool):
            operand = Constant(operand)

        self.operand = operand
        self.op = op

    def __str__(self) -> str:
        return f"({self.op}{self.operand})"

    @property
    def variables(self) -> set[str]:
        return self.operand.variables

    def evaluate(self, bindings: dict[str, bool]) -> bool:
        if self.op == "~":
            return not self.operand.evaluate(bindings)

        raise ValueError(f"unknown unary operator: {self.op}")


class BinaryOperation(Expression):
    def __init__(self, left: Expression | bool, op: str, right: Expression | bool):
        if not isinstance(left, (bool, Expression)):
            raise ValueError(f"invalid left operand type: {type(left).__name__!r}")

        if not isinstance(right, (bool, Expression)):
            raise ValueError(f"invalid right operand type: {type(right).__name__!r}")

        if isinstance(left, bool):
            left = Constant(left)

        if isinstance(right, bool):
            right = Constant(right)

        self.left = left
        self.op = op
        self.right = right

    def __str__(self) -> str:
        return f"({self.left} {self.op} {self.right})"

    @property
    def variables(self) -> set[str]:
        return self.left.variables | self.right.variables

    def evaluate(self, bindings: dict[str, bool]) -> bool:
        left_val = self.left.evaluate(bindings)
        right_val = self.right.evaluate(bindings)

        match self.op:
            case self.AND:
                return left_val and right_val
            case self.OR:
                return left_val or right_val
            case self.XOR:
                return left_val ^ right_val

        raise ValueError(f"unknown binary operator: {self.op}")


TRUE = Constant(True)
FALSE = Constant(False)
