"""Unit tests for the arithmetic expression and equation engine.

This module validates construction, string representation, variable extraction,
evaluation, operator overloads, substitution, and guard clauses of all arithmetic
expression classes and the Equation class defined in `engine.equation`.
"""

import pytest

from demorganizer.core import Number
from demorganizer.engine import ArithmeticBinaryOperation, ArithmeticUnaryOperation, Equation, NumericConstant, NumericVariable


# -----------------------------------------------------------------------------
# Reference instances and constants
# -----------------------------------------------------------------------------

VAR_X: NumericVariable = NumericVariable("x")
"""A reusable numeric variable named 'x'."""

VAR_Y: NumericVariable = NumericVariable("y")
"""A reusable numeric variable named 'y'."""

CONST_ZERO: NumericConstant = NumericConstant(0)
"""A numeric constant with value 0."""

CONST_ONE: NumericConstant = NumericConstant(1)
"""A numeric constant with value 1."""

CONST_FIVE: NumericConstant = NumericConstant(5)
"""A numeric constant with value 5."""

BINDINGS_XY: dict[str, Number] = {"x": 3, "y": 2}
"""Bindings where x=3 and y=2."""


# -----------------------------------------------------------------------------
# NumericVariable
# -----------------------------------------------------------------------------


class TestNumericVariable:
    def test_str_returns_name(self) -> None:
        """Asserts that the string representation of a variable is its name."""

        assert str(VAR_X) == "x"

    def test_variables_returns_singleton_set(self) -> None:
        """Asserts that the variables property returns a set containing only this variable's name."""

        assert VAR_X.variables == {"x"}

    @pytest.mark.parametrize("bindings, expected", [({"x": 5}, 5), ({"x": -3.14}, -3.14)])
    def test_evaluate_returns_bound_value(self, bindings: dict[str, Number], expected: Number) -> None:
        """Asserts that evaluate returns the value bound to the variable's name."""

        assert VAR_X.evaluate(bindings) == expected

    def test_evaluate_raises_value_error_when_missing_binding(self) -> None:
        """Asserts that evaluate raises a ValueError when the variable's name is not in the bindings."""

        with pytest.raises(ValueError, match="Missing binding"):
            VAR_X.evaluate({})


# -----------------------------------------------------------------------------
# NumericConstant
# -----------------------------------------------------------------------------


class TestNumericConstant:
    @pytest.mark.parametrize("value, expected_str", [(42, "42"), (3.14, "3.14"), (0, "0")])
    def test_str_returns_numeric_value(self, value: Number, expected_str: str) -> None:
        """Asserts that the string representation matches the numeric value."""

        assert str(NumericConstant(value)) == expected_str

    def test_variables_returns_empty_set(self) -> None:
        """Asserts that constants contain no variables."""

        assert CONST_FIVE.variables == set()

    @pytest.mark.parametrize("value", [0, 1, -7, 3.14])
    def test_evaluate_returns_fixed_value(self, value: Number) -> None:
        """Asserts that evaluate always returns the constant's fixed value regardless of bindings."""

        assert NumericConstant(value).evaluate({"x": 999}) == value


# -----------------------------------------------------------------------------
# ArithmeticUnaryOperation
# -----------------------------------------------------------------------------


class TestArithmeticUnaryOperation:
    def test_str_returns_parenthesised_negation(self) -> None:
        """Asserts that the string representation wraps the operand with the negation operator."""

        assert str(-VAR_X) == "(-x)"

    def test_variables_returns_operand_variables(self) -> None:
        """Asserts that variables returns the set of variables from the inner operand."""

        assert (-VAR_X).variables == {"x"}

    @pytest.mark.parametrize("bindings, expected", [({"x": 5}, -5), ({"x": -3}, 3)])
    def test_evaluate_negates_operand(self, bindings: dict[str, Number], expected: Number) -> None:
        """Asserts that the negation operator correctly negates the operand's evaluated value."""

        assert (-VAR_X).evaluate(bindings) == expected


# -----------------------------------------------------------------------------
# ArithmeticBinaryOperation
# -----------------------------------------------------------------------------


class TestArithmeticBinaryOperation:
    def test_str_returns_parenthesised_infix(self) -> None:
        """Asserts that the string representation uses parenthesised infix notation."""

        assert str(VAR_X + CONST_ONE) == "(x + 1)"

    def test_variables_returns_union_of_operands(self) -> None:
        """Asserts that variables returns the union of variables from both operands."""

        assert (VAR_X + VAR_Y).variables == {"x", "y"}

    def test_add_evaluates_correctly(self) -> None:
        """Asserts that addition evaluates to the sum of both operands."""

        assert (VAR_X + VAR_Y).evaluate(BINDINGS_XY) == 5

    def test_sub_evaluates_correctly(self) -> None:
        """Asserts that subtraction evaluates to the difference of both operands."""

        assert (VAR_X - VAR_Y).evaluate(BINDINGS_XY) == 1

    def test_mul_evaluates_correctly(self) -> None:
        """Asserts that multiplication evaluates to the product of both operands."""

        assert (VAR_X * VAR_Y).evaluate(BINDINGS_XY) == 6

    def test_div_evaluates_correctly(self) -> None:
        """Asserts that division evaluates to the quotient of both operands."""

        assert (VAR_X / VAR_Y).evaluate(BINDINGS_XY) == 1.5

    def test_div_raises_zero_division_when_divisor_is_zero(self) -> None:
        """Asserts that division raises a ZeroDivisionError when the right operand evaluates to zero."""

        with pytest.raises(ZeroDivisionError, match="Division by zero"):
            (VAR_X / CONST_ZERO).evaluate({"x": 5})


# -----------------------------------------------------------------------------
# Arithmetic operator overloads
# -----------------------------------------------------------------------------


class TestArithmeticOperatorOverloads:
    def test_operator_with_number_wraps_in_constant(self) -> None:
        """Asserts that using a raw number with an operator wraps it in a NumericConstant."""

        result = VAR_X + 1

        assert isinstance(result, ArithmeticBinaryOperation)
        assert result.evaluate({"x": 4}) == 5

    def test_reverse_add_with_number(self) -> None:
        """Asserts that reverse addition (number + expression) builds the correct tree."""

        result = 10 + VAR_X

        assert isinstance(result, ArithmeticBinaryOperation)
        assert result.evaluate({"x": 3}) == 13

    def test_reverse_sub_with_number(self) -> None:
        """Asserts that reverse subtraction (number - expression) builds the correct tree."""

        result = 10 - VAR_X

        assert isinstance(result, ArithmeticBinaryOperation)
        assert result.evaluate({"x": 3}) == 7

    def test_eq_operator_creates_equation(self) -> None:
        """Asserts that the == operator between expressions creates an Equation instance."""

        result = VAR_X == CONST_FIVE

        assert isinstance(result, Equation)

    def test_operator_with_invalid_type_returns_not_implemented(self) -> None:
        """Asserts that using an unsupported type with an operator returns NotImplemented."""

        result = VAR_X.__add__("invalid")

        assert result is NotImplemented


# -----------------------------------------------------------------------------
# Equation
# -----------------------------------------------------------------------------


class TestEquation:
    def test_str_returns_lhs_equals_rhs(self) -> None:
        """Asserts that the string representation shows both sides separated by '='."""

        eq = VAR_X == CONST_FIVE

        assert str(eq) == "x = 5"

    def test_repr_returns_detailed_string(self) -> None:
        """Asserts that repr includes the Equation class name with both sides."""

        eq = VAR_X == CONST_FIVE

        assert repr(eq) == "Equation(x, 5)"

    def test_variables_returns_union_of_both_sides(self) -> None:
        """Asserts that variables returns the union of variables from lhs and rhs."""

        eq = Equation(VAR_X + VAR_Y, CONST_FIVE)

        assert eq.variables == {"x", "y"}

    def test_evaluate_returns_true_when_satisfied(self) -> None:
        """Asserts that evaluate returns True when lhs equals rhs under the given bindings."""

        eq = VAR_X == CONST_FIVE

        assert eq.evaluate({"x": 5}) is True

    def test_evaluate_returns_false_when_not_satisfied(self) -> None:
        """Asserts that evaluate returns False when lhs does not equal rhs under the given bindings."""

        eq = VAR_X == CONST_FIVE

        assert eq.evaluate({"x": 3}) is False

    def test_add_applies_to_both_sides(self) -> None:
        """Asserts that adding a value to an equation applies it to both sides equally."""

        eq = VAR_X == CONST_FIVE
        shifted = eq + 1

        assert shifted.evaluate({"x": 5}) is True

    def test_substitute_replaces_variable(self) -> None:
        """Asserts that substitute replaces the target variable in both sides of the equation."""

        eq = Equation(VAR_X + VAR_Y, NumericConstant(10))
        substituted = eq.substitute("x", NumericConstant(3))

        assert substituted.evaluate({"y": 7}) is True

    def test_init_raises_value_error_when_invalid_operand(self) -> None:
        """Asserts that constructing an Equation with an unsupported type raises a ValueError."""

        with pytest.raises(ValueError, match="Invalid"):
            Equation("not_an_expression", VAR_X)  # type: ignore[arg-type]
