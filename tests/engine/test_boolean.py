"""Unit tests for the boolean expression engine.

This module validates construction, string representation, variable extraction,
evaluation, operator overloads, and guard clauses of all boolean expression
classes defined in `engine.boolean`.
"""

import pytest

from demorganizer.engine import BooleanBinaryOperation, BooleanConstant, BooleanUnaryOperation, BooleanVariable


# -----------------------------------------------------------------------------
# Reference instances and constants
# -----------------------------------------------------------------------------

VAR_A: BooleanVariable = BooleanVariable("A")
"""A reusable variable instance named 'A'."""

VAR_B: BooleanVariable = BooleanVariable("B")
"""A reusable variable instance named 'B'."""

TRUE: BooleanConstant = BooleanConstant(True)
"""A constant representing the boolean value True."""

FALSE: BooleanConstant = BooleanConstant(False)
"""A constant representing the boolean value False."""

BINDINGS_TT: dict[str, bool] = {"A": True, "B": True}
"""Bindings where both A and B are True."""

BINDINGS_TF: dict[str, bool] = {"A": True, "B": False}
"""Bindings where A is True and B is False."""

BINDINGS_FT: dict[str, bool] = {"A": False, "B": True}
"""Bindings where A is False and B is True."""

BINDINGS_FF: dict[str, bool] = {"A": False, "B": False}
"""Bindings where both A and B are False."""


# -----------------------------------------------------------------------------
# BooleanVariable
# -----------------------------------------------------------------------------


class TestBooleanVariable:
    def test_str_returns_name(self) -> None:
        """Asserts that the string representation of a variable is its single-character name."""

        assert str(VAR_A) == "A"

    def test_variables_returns_singleton_set(self) -> None:
        """Asserts that the variables property returns a set containing only this variable's name."""

        assert VAR_A.variables == {"A"}

    @pytest.mark.parametrize("bindings, expected", [({"A": True}, True), ({"A": False}, False)])
    def test_evaluate_returns_bound_value(self, bindings: dict[str, bool], expected: bool) -> None:
        """Asserts that evaluate returns the value bound to the variable's name."""

        assert VAR_A.evaluate(bindings) == expected

    def test_evaluate_raises_value_error_when_missing_binding(self) -> None:
        """Asserts that evaluate raises a ValueError when the variable's name is not in the bindings."""

        with pytest.raises(ValueError, match="Missing binding"):
            VAR_A.evaluate({})

    @pytest.mark.parametrize("invalid_name", ["AB", "1", "", "ab"])
    def test_init_raises_value_error_when_invalid_name(self, invalid_name: str) -> None:
        """Asserts that constructing a variable with an invalid name raises a ValueError."""

        with pytest.raises(ValueError, match="single alphabetic character"):
            BooleanVariable(invalid_name)


# -----------------------------------------------------------------------------
# BooleanConstant
# -----------------------------------------------------------------------------


class TestBooleanConstant:
    @pytest.mark.parametrize("constant, expected_str", [(TRUE, "1"), (FALSE, "0")])
    def test_str_returns_one_or_zero(self, constant: BooleanConstant, expected_str: str) -> None:
        """Asserts that the string representation is '1' for True and '0' for False."""

        assert str(constant) == expected_str

    def test_variables_returns_empty_set(self) -> None:
        """Asserts that constants contain no variables."""

        assert TRUE.variables == set()

    @pytest.mark.parametrize("value, expected", [(True, True), (False, False)])
    def test_evaluate_returns_fixed_value(self, value: bool, expected: bool) -> None:
        """Asserts that evaluate always returns the constant's fixed value."""

        assert BooleanConstant(value).evaluate({}) == expected

    def test_evaluate_ignores_bindings(self) -> None:
        """Asserts that evaluate returns the same result regardless of the bindings provided."""

        assert TRUE.evaluate({"A": False}) is True


# -----------------------------------------------------------------------------
# BooleanUnaryOperation
# -----------------------------------------------------------------------------


class TestBooleanUnaryOperation:
    def test_str_returns_parenthesised_expression(self) -> None:
        """Asserts that the string representation wraps the operand in parentheses with the operator."""

        assert str(~VAR_A) == "(~A)"

    def test_variables_returns_operand_variables(self) -> None:
        """Asserts that variables returns the set of variables from the inner operand."""

        assert (~VAR_A).variables == {"A"}

    @pytest.mark.parametrize("bindings, expected", [({"A": True}, False), ({"A": False}, True)])
    def test_evaluate_negates_operand(self, bindings: dict[str, bool], expected: bool) -> None:
        """Asserts that the NOT operator correctly negates the operand's evaluated value."""

        assert (~VAR_A).evaluate(bindings) == expected

    def test_invert_operator_creates_unary_operation(self) -> None:
        """Asserts that the ~ operator on a BooleanExpression produces a BooleanUnaryOperation."""

        result = ~VAR_A

        assert isinstance(result, BooleanUnaryOperation)


# -----------------------------------------------------------------------------
# BooleanBinaryOperation
# -----------------------------------------------------------------------------


class TestBooleanBinaryOperation:
    def test_str_returns_parenthesised_infix(self) -> None:
        """Asserts that the string representation uses parenthesised infix notation."""

        assert str(VAR_A & VAR_B) == "(A & B)"

    def test_variables_returns_union_of_operands(self) -> None:
        """Asserts that variables returns the union of variables from both operands."""

        assert (VAR_A & VAR_B).variables == {"A", "B"}

    @pytest.mark.parametrize("bindings, expected", [(BINDINGS_TT, True), (BINDINGS_TF, False), (BINDINGS_FT, False), (BINDINGS_FF, False)])
    def test_and_evaluates_correctly(self, bindings: dict[str, bool], expected: bool) -> None:
        """Asserts that the AND operator produces the correct truth-table result."""

        assert (VAR_A & VAR_B).evaluate(bindings) == expected

    @pytest.mark.parametrize("bindings, expected", [(BINDINGS_TT, True), (BINDINGS_TF, True), (BINDINGS_FT, True), (BINDINGS_FF, False)])
    def test_or_evaluates_correctly(self, bindings: dict[str, bool], expected: bool) -> None:
        """Asserts that the OR operator produces the correct truth-table result."""

        assert (VAR_A | VAR_B).evaluate(bindings) == expected

    @pytest.mark.parametrize("bindings, expected", [(BINDINGS_TT, False), (BINDINGS_TF, True), (BINDINGS_FT, True), (BINDINGS_FF, False)])
    def test_xor_evaluates_correctly(self, bindings: dict[str, bool], expected: bool) -> None:
        """Asserts that the XOR operator produces the correct truth-table result."""

        assert (VAR_A ^ VAR_B).evaluate(bindings) == expected

    def test_operator_with_bool_wraps_in_constant(self) -> None:
        """Asserts that using a raw bool with an operator wraps it in a BooleanConstant."""

        result = VAR_A & True

        assert isinstance(result, BooleanBinaryOperation)
        assert result.evaluate({"A": True}) is True

    def test_operator_with_invalid_type_returns_not_implemented(self) -> None:
        """Asserts that using an unsupported type with an operator returns NotImplemented."""

        result = VAR_A.__and__(42)

        assert result is NotImplemented
