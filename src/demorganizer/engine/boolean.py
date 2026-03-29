from abc import ABC, abstractmethod


class BooleanExpression(ABC):
    """Abstract base class for all boolean expressions."""

    AND = "&"
    OR = "|"
    XOR = "^"
    NOT = "~"

    def __and__(self, other: "BooleanExpression | bool") -> "BooleanBinaryOperation":
        if isinstance(other, bool):
            return BooleanBinaryOperation(self, self.AND, BooleanConstant(other))

        if not isinstance(other, BooleanExpression):
            return NotImplemented

        return BooleanBinaryOperation(self, self.AND, other)

    def __or__(self, other: "BooleanExpression | bool") -> "BooleanBinaryOperation":
        if isinstance(other, bool):
            return BooleanBinaryOperation(self, self.OR, other)

        if not isinstance(other, BooleanExpression):
            return NotImplemented

        return BooleanBinaryOperation(self, self.OR, other)

    def __xor__(self, other: "BooleanExpression | bool") -> "BooleanBinaryOperation":
        if isinstance(other, bool):
            return BooleanBinaryOperation(self, self.XOR, other)

        if not isinstance(other, BooleanExpression):
            return NotImplemented

        return BooleanBinaryOperation(self, self.XOR, other)

    def __invert__(self) -> "BooleanUnaryOperation":
        return BooleanUnaryOperation(self.NOT, self)

    @abstractmethod
    def evaluate(self, bindings: dict[str, bool]) -> bool:
        """Evaluates the expression with a given set of variable values."""

        raise NotImplementedError

    @property
    @abstractmethod
    def variables(self) -> set[str]:
        """Recursively finds all unique variables in the"""

        raise NotImplementedError


class BooleanVariable(BooleanExpression):
    """A boolean expression representing a named, single-character variable."""

    def __init__(self, name: str):
        """Initializes the variable, raising ValueError if name is not a single letter."""

        if not name.isalpha() or len(name) != 1:
            raise ValueError("Variable name must be a single alphabetic character.")

        self.name = name

    def __str__(self) -> str:
        """Returns the variable's single-character name."""

        return self.name

    @property
    def variables(self) -> set[str]:
        """Returns a set containing only this variable's name."""

        return {self.name}

    def evaluate(self, bindings: dict[str, bool]) -> bool:
        """Returns the value bound to this variable's name, raising ValueError if absent."""

        if self.name not in bindings:
            raise ValueError(f"Missing binding for variable: {self.name!r}")

        return bindings[self.name]


class BooleanConstant(BooleanExpression):
    """A boolean expression that always evaluates to a fixed truth value."""

    def __init__(self, value: bool):
        """Initializes the constant with its fixed boolean value."""

        self.value = value

    def __str__(self) -> str:
        """Returns '1' for True and '0' for False."""

        return {True: "1", False: "0"}[self.value]

    @property
    def variables(self) -> set[str]:
        """Returns an empty set, as constants contain no variables."""

        return set()

    def evaluate(self, bindings: dict[str, bool]) -> bool:
        """Returns the constant's fixed value, ignoring any bindings."""

        return self.value


class BooleanUnaryOperation(BooleanExpression):
    """A boolean expression applying a unary operator to a single operand."""

    def __init__(self, op: str, operand: BooleanExpression | bool):
        """Initializes the operation, wrapping bare booleans in a"""

        if not isinstance(operand, (bool, BooleanExpression)):
            raise ValueError(f"Invalid operand type: {type(operand).__name__!r}")

        if isinstance(operand, bool):
            operand = BooleanConstant(operand)

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


class BooleanBinaryOperation(BooleanExpression):
    """A boolean expression applying a binary operator to two operands."""

    def __init__(self, left: BooleanExpression | bool, op: str, right: BooleanExpression | bool):
        """Initializes the operation, wrapping bare booleans in Constants."""

        if not isinstance(left, (bool, BooleanExpression)):
            raise ValueError(f"Invalid left operand type: {type(left).__name__!r}")

        if not isinstance(right, (bool, BooleanExpression)):
            raise ValueError(f"Invalid right operand type: {type(right).__name__!r}")

        if isinstance(left, bool):
            left = BooleanConstant(left)

        if isinstance(right, bool):
            right = BooleanConstant(right)

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
