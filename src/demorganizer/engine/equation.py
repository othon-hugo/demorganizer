from __future__ import annotations

from abc import ABC, abstractmethod

from demorganizer.core import Number


class Equation:
    """Represents an equation: lhs = rhs. Operators manipulate both sides."""

    def __init__(self, lhs: ArithmeticExpression | int | float, rhs: ArithmeticExpression | int | float):
        """Initializes the equation, wrapping bare numbers in NumericConstant."""

        if isinstance(lhs, (int, float)):
            lhs = NumericConstant(lhs)

        if isinstance(rhs, (int, float)):
            rhs = NumericConstant(rhs)

        if not isinstance(lhs, ArithmeticExpression):
            raise ValueError(f"Invalid left-hand side type: {type(lhs).__name__!r}")

        if not isinstance(rhs, ArithmeticExpression):
            raise ValueError(f"Invalid right-hand side type: {type(rhs).__name__!r}")

        self.lhs = lhs
        self.rhs = rhs

    def __str__(self) -> str:
        """Returns the equation as 'lhs = rhs'."""

        return f"{self.lhs} = {self.rhs}"

    def __repr__(self) -> str:
        """Returns a detailed string representation."""

        return f"Equation({self.lhs}, {self.rhs})"

    def __add__(self, other: ArithmeticExpression | int | float) -> Equation:
        """Adds to both sides: (lhs + other) = (rhs + other)."""

        return Equation(self.lhs + other, self.rhs + other)

    def __sub__(self, other: ArithmeticExpression | int | float) -> Equation:
        """Subtracts from both sides: (lhs - other) = (rhs - other)."""

        return Equation(self.lhs - other, self.rhs - other)

    def __mul__(self, other: ArithmeticExpression | int | float) -> Equation:
        """Multiplies both sides: (lhs * other) = (rhs * other)."""

        return Equation(self.lhs * other, self.rhs * other)

    def __truediv__(self, other: ArithmeticExpression | int | float) -> Equation:
        """Divides both sides: (lhs / other) = (rhs / other)."""

        return Equation(self.lhs / other, self.rhs / other)

    def __neg__(self) -> Equation:
        """Negates both sides: (-lhs) = (-rhs)."""

        return Equation(-self.lhs, -self.rhs)

    def evaluate(self, bindings: dict[str, Number]) -> bool:
        """Returns True if lhs equals rhs under the given bindings."""

        return self.lhs.evaluate(bindings) == self.rhs.evaluate(bindings)

    def substitute(self, var: str, value: ArithmeticExpression | int | float) -> Equation:
        """Replaces a variable with a value or expression in both sides."""

        return Equation(_substitute_expr(self.lhs, var, value), _substitute_expr(self.rhs, var, value))

    @property
    def variables(self) -> set[str]:
        """Returns the union of variables present in both sides."""

        return self.lhs.variables | self.rhs.variables


class ArithmeticExpression(ABC):
    """Abstract base class for all arithmetic expressions."""

    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"
    NEG = "-"

    def __add__(self, other: ArithmeticExpression | Number) -> ArithmeticBinaryOperation:
        """Builds an addition node: self + other."""

        if isinstance(other, (int, float)):
            return ArithmeticBinaryOperation(self, self.ADD, NumericConstant(other))

        if not isinstance(other, ArithmeticExpression):
            return NotImplemented

        return ArithmeticBinaryOperation(self, self.ADD, other)

    def __radd__(self, other: Number) -> ArithmeticBinaryOperation:
        """Builds an addition node: other + self (reverse)."""

        if isinstance(other, (int, float)):
            return ArithmeticBinaryOperation(NumericConstant(other), self.ADD, self)

        return NotImplemented

    def __sub__(self, other: ArithmeticExpression | Number) -> ArithmeticBinaryOperation:
        """Builds a subtraction node: self - other."""

        if isinstance(other, (int, float)):
            return ArithmeticBinaryOperation(self, self.SUB, NumericConstant(other))

        if not isinstance(other, ArithmeticExpression):
            return NotImplemented

        return ArithmeticBinaryOperation(self, self.SUB, other)

    def __rsub__(self, other: Number) -> ArithmeticBinaryOperation:
        """Builds a subtraction node: other - self (reverse)."""

        if isinstance(other, (int, float)):
            return ArithmeticBinaryOperation(NumericConstant(other), self.SUB, self)

        return NotImplemented

    def __mul__(self, other: ArithmeticExpression | Number) -> ArithmeticBinaryOperation:
        """Builds a multiplication node: self * other."""

        if isinstance(other, (int, float)):
            return ArithmeticBinaryOperation(self, self.MUL, NumericConstant(other))

        if not isinstance(other, ArithmeticExpression):
            return NotImplemented

        return ArithmeticBinaryOperation(self, self.MUL, other)

    def __rmul__(self, other: Number) -> ArithmeticBinaryOperation:
        """Builds a multiplication node: other * self (reverse)."""

        if isinstance(other, (int, float)):
            return ArithmeticBinaryOperation(NumericConstant(other), self.MUL, self)

        return NotImplemented

    def __truediv__(self, other: ArithmeticExpression | Number) -> ArithmeticBinaryOperation:
        """Builds a division node: self / other."""

        if isinstance(other, (int, float)):
            return ArithmeticBinaryOperation(self, self.DIV, NumericConstant(other))

        if not isinstance(other, ArithmeticExpression):
            return NotImplemented

        return ArithmeticBinaryOperation(self, self.DIV, other)

    def __rtruediv__(self, other: Number) -> ArithmeticBinaryOperation:
        """Builds a division node: other / self (reverse)."""

        if isinstance(other, (int, float)):
            return ArithmeticBinaryOperation(NumericConstant(other), self.DIV, self)

        return NotImplemented

    def __neg__(self) -> ArithmeticUnaryOperation:
        """Builds a negation node: -self."""

        return ArithmeticUnaryOperation(self.NEG, self)

    def __eq__(self, other: object) -> Equation:  # type: ignore[override]
        """Creates an Equation: self = other."""

        if isinstance(other, (int, float)):
            return Equation(self, NumericConstant(other))

        if isinstance(other, ArithmeticExpression):
            return Equation(self, other)

        return NotImplemented

    def __hash__(self) -> int:
        """Identity-based hash, required since __eq__ is overridden."""

        return id(self)

    @abstractmethod
    def evaluate(self, bindings: dict[str, Number]) -> Number:
        """Evaluates the expression with a given set of variable values."""

        raise NotImplementedError

    @property
    @abstractmethod
    def variables(self) -> set[str]:
        """Recursively finds all unique variables in the expression."""

        raise NotImplementedError


class NumericVariable(ArithmeticExpression):
    """A named numeric variable."""

    def __init__(self, name: str):
        """Initializes the variable with its name."""

        if not name.isalpha():
            raise ValueError("Variable name must contain only alphabetic characters.")

        self.name = name

    def __str__(self) -> str:
        """Returns the variable's name."""

        return self.name

    @property
    def variables(self) -> set[str]:
        """Returns a set containing only this variable's name."""

        return {self.name}

    def evaluate(self, bindings: dict[str, Number]) -> Number:
        """Returns the value bound to this variable's name, raising ValueError if absent."""

        if self.name not in bindings:
            raise ValueError(f"Missing binding for variable: {self.name!r}")

        return bindings[self.name]


class NumericConstant(ArithmeticExpression):
    """A fixed numeric value (int or float)."""

    def __init__(self, value: Number):
        """Initializes the constant with its fixed numeric value."""

        self.value = value

    def __str__(self) -> str:
        """Returns the string representation of the numeric value."""

        return str(self.value)

    @property
    def variables(self) -> set[str]:
        """Returns an empty set, as constants contain no variables."""

        return set()

    def evaluate(self, bindings: dict[str, Number]) -> Number:
        """Returns the constant's fixed value, ignoring any bindings."""

        return self.value


class ArithmeticUnaryOperation(ArithmeticExpression):
    """A unary arithmetic operation applied to a single operand."""

    def __init__(self, op: str, operand: ArithmeticExpression | int | float):
        """Initializes the operation, wrapping bare numbers in NumericConstant."""

        if isinstance(operand, (int, float)):
            operand = NumericConstant(operand)

        if not isinstance(operand, ArithmeticExpression):
            raise ValueError(f"Invalid operand type: {type(operand).__name__!r}")

        self.op = op
        self.operand = operand

    def __str__(self) -> str:
        """Returns the expression as a parenthesised string, e.g. '(-x)'."""

        return f"({self.op}{self.operand})"

    @property
    def variables(self) -> set[str]:
        """Returns the set of variables present in the operand."""

        return self.operand.variables

    def evaluate(self, bindings: dict[str, Number]) -> Number:
        """Evaluates the unary operation."""

        if self.op == self.NEG:
            return -self.operand.evaluate(bindings)

        raise ValueError(f"Unknown unary operator: {self.op!r}")


class ArithmeticBinaryOperation(ArithmeticExpression):
    """A binary arithmetic operation applied to two operands."""

    def __init__(self, left: ArithmeticExpression | int | float, op: str, right: ArithmeticExpression | int | float):
        """Initializes the operation, wrapping bare numbers in NumericConstant."""

        if isinstance(left, (int, float)):
            left = NumericConstant(left)

        if isinstance(right, (int, float)):
            right = NumericConstant(right)

        if not isinstance(left, ArithmeticExpression):
            raise ValueError(f"Invalid left operand type: {type(left).__name__!r}")

        if not isinstance(right, ArithmeticExpression):
            raise ValueError(f"Invalid right operand type: {type(right).__name__!r}")

        self.left = left
        self.op = op
        self.right = right

    def __str__(self) -> str:
        """Returns the expression as a parenthesised infix string, e.g. '(x + 1)'."""

        return f"({self.left} {self.op} {self.right})"

    @property
    def variables(self) -> set[str]:
        """Returns the union of variables present in both operands."""

        return self.left.variables | self.right.variables

    def evaluate(self, bindings: dict[str, Number]) -> Number:
        """Evaluates both operands and applies the operator."""

        left_val = self.left.evaluate(bindings)
        right_val = self.right.evaluate(bindings)

        match self.op:
            case self.ADD:
                return left_val + right_val
            case self.SUB:
                return left_val - right_val
            case self.MUL:
                return left_val * right_val
            case self.DIV:
                if right_val == 0:
                    raise ZeroDivisionError("Division by zero in expression.")
                return left_val / right_val

        raise ValueError(f"Unknown arithmetic operator: {self.op!r}")


def _substitute_expr(expr: ArithmeticExpression, var: str, value: ArithmeticExpression | int | float) -> ArithmeticExpression:
    """Recursively substitutes a variable with a value in an expression tree."""

    if isinstance(value, (int, float)):
        value = NumericConstant(value)

    if isinstance(expr, NumericConstant):
        return expr

    if isinstance(expr, NumericVariable):
        return value if expr.name == var else expr

    if isinstance(expr, ArithmeticBinaryOperation):
        return ArithmeticBinaryOperation(
            _substitute_expr(expr.left, var, value),
            expr.op,
            _substitute_expr(expr.right, var, value),
        )

    if isinstance(expr, ArithmeticUnaryOperation):
        return ArithmeticUnaryOperation(expr.op, _substitute_expr(expr.operand, var, value))

    raise TypeError(f"Unknown expression type: {type(expr).__name__!r}")
