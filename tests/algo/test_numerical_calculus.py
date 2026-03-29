"""Unit tests for the numerical calculus algorithms.

This module validates the convergence, monotonic properties, error bounds,
and guard clauses of all iterative numerical methods defined in `algo.numerical_calculus`.
"""

import pytest

from demorganizer.algo import calculate_bisection_steps, iter_bisection, iter_false_position, iter_linear_iteration, iter_newton_raphson, iter_secant
from demorganizer.core import Interval, Number, UnaryFunction

# -----------------------------------------------------------------------------
# Reference functions and constants
# -----------------------------------------------------------------------------

SQRT2: float = 2**0.5
"""The exact positive root of x^2 - 2 = 0."""

CBRT_OF_SHIFTED: float = 1.52138
"""An approximate root for x^3 - x - 2 = 0, used to test convergence on polynomials."""

TOLERANCE: float = 1e-6
"""The acceptable error margin for numerical convergence tests."""

STEPS: int = 50
"""The standard fixed number of iterations to guarantee convergence for most methods."""

SECANT_STEPS: int = 8
"""Restricted step limit for the secant method, which saturates to machine epsilon quickly given our inputs."""

F_QUADRATIC: UnaryFunction = lambda x: x**2 - 2
"""A standard quadratic reference function with a root at √2 and a sign change in [1, 2]."""

F_CUBIC: UnaryFunction = lambda x: x**3 - x - 2
"""A cubic reference function with a root near 1.52138 and a sign change in [1, 2]."""

F_SAME_SIGN: UnaryFunction = lambda x: x**2 + 1
"""A strictly positive reference function with no real roots (never crosses the x-axis)."""

DF_QUADRATIC: UnaryFunction = lambda x: 2 * x
"""The exact analytical derivative of F_QUADRATIC(x)."""

DF_ZERO: UnaryFunction = lambda x: 0.0
"""A constant zero derivative used to test the ZeroDivisionError guard in Newton-Raphson."""

PHI_SQRT2: UnaryFunction = lambda x: (x + 2 / x) / 2
"""The fixed-point iteration form of F_QUADRATIC, where x = phi(x) yields the root √2."""


# -----------------------------------------------------------------------------
# iter_bisection
# -----------------------------------------------------------------------------


class TestIterBisection:
    @pytest.mark.parametrize("f, interval, expected_root", [(F_QUADRATIC, (1.0, 2.0), SQRT2), (F_CUBIC, (1.0, 2.0), CBRT_OF_SHIFTED)])
    def test_converges_to_root(self, f: UnaryFunction, interval: Interval, expected_root: Number) -> None:
        """Asserts that the bisection method converges to the expected root within the tolerance."""

        *_, last = iter_bisection(f, interval, steps=STEPS)

        assert abs(last - expected_root) < TOLERANCE

    def test_yields_exactly_n_steps(self) -> None:
        """Asserts that the bisection method yields exactly the requested number of estimates."""

        estimates = list(iter_bisection(F_QUADRATIC, (1.0, 2.0), steps=10))

        assert len(estimates) == 10

    def test_raises_value_error_when_same_sign(self) -> None:
        """Asserts that bisection raises a ValueError when interval endpoints evaluate to the same sign."""

        with pytest.raises(ValueError, match="opposite signs"):
            list(iter_bisection(F_SAME_SIGN, (1.0, 2.0), steps=10))


# -----------------------------------------------------------------------------
# calculate_bisection_steps
# -----------------------------------------------------------------------------


class TestCalculateBisectionSteps:
    def test_returns_positive_integer(self) -> None:
        """Asserts that the calculated number of steps is a strictly positive integer."""

        result = calculate_bisection_steps(precision=1e-6, interval=(1.0, 2.0))

        assert isinstance(result, int) and result > 0

    def test_higher_precision_requires_more_steps(self) -> None:
        """Asserts that requesting a higher precision results in a larger number of required iterations."""

        coarse = calculate_bisection_steps(precision=1e-3, interval=(1.0, 2.0))
        fine = calculate_bisection_steps(precision=1e-9, interval=(1.0, 2.0))

        assert fine > coarse

    @pytest.mark.parametrize("precision, interval", [(1e-6, (1.0, 2.0)), (1e-4, (0.0, 4.0))])
    def test_sufficient_steps_achieve_precision(self, precision: float, interval: Interval) -> None:
        """Asserts that running bisection for the calculated number of steps successfully hits the target precision."""

        n = calculate_bisection_steps(precision=precision, interval=interval)
        *_, last = iter_bisection(F_QUADRATIC, interval, steps=n)

        assert abs(last - SQRT2) < precision


# -----------------------------------------------------------------------------
# iter_false_position
# -----------------------------------------------------------------------------


class TestIterFalsePosition:
    @pytest.mark.parametrize("f, interval, expected_root", [(F_QUADRATIC, (1.0, 2.0), SQRT2), (F_CUBIC, (1.0, 2.0), CBRT_OF_SHIFTED)])
    def test_converges_to_root(self, f: UnaryFunction, interval: Interval, expected_root: Number) -> None:
        """Asserts that the false-position method converges to the expected root within the tolerance."""

        *_, last = iter_false_position(f, interval, steps=STEPS)

        assert abs(last - expected_root) < TOLERANCE

    def test_yields_exactly_n_steps(self) -> None:
        """Asserts that the false-position method yields exactly the requested number of estimates."""

        estimates = list(iter_false_position(F_QUADRATIC, (1.0, 2.0), steps=10))

        assert len(estimates) == 10

    def test_raises_value_error_when_same_sign(self) -> None:
        """Asserts that false-position raises a ValueError when interval endpoints evaluate to the same sign."""

        with pytest.raises(ValueError, match="opposite signs"):
            list(iter_false_position(F_SAME_SIGN, (1.0, 2.0), steps=10))


# -----------------------------------------------------------------------------
# iter_newton_raphson
# -----------------------------------------------------------------------------


class TestIterNewtonRaphson:
    @pytest.mark.parametrize("f, df, x0, expected_root", [(F_QUADRATIC, DF_QUADRATIC, 1.5, SQRT2)])
    def test_converges_to_root(self, f: UnaryFunction, df: UnaryFunction, x0: Number, expected_root: Number) -> None:
        """Asserts that the Newton-Raphson method converges to the expected root within the tolerance."""

        *_, last = iter_newton_raphson(f, df, x0=x0, steps=STEPS)

        assert abs(last - expected_root) < TOLERANCE

    def test_yields_exactly_n_steps(self) -> None:
        """Asserts that the Newton-Raphson method yields exactly the requested number of estimates."""

        estimates = list(iter_newton_raphson(F_QUADRATIC, DF_QUADRATIC, x0=1.5, steps=10))

        assert len(estimates) == 10

    def test_raises_zero_division_when_derivative_is_zero(self) -> None:
        """Asserts that Newton-Raphson raises a ZeroDivisionError if the derivative evaluates to zero."""

        with pytest.raises(ZeroDivisionError, match="Derivative is zero"):
            list(iter_newton_raphson(F_QUADRATIC, DF_ZERO, x0=1.5, steps=5))


# -----------------------------------------------------------------------------
# iter_secant
# -----------------------------------------------------------------------------


class TestIterSecant:
    @pytest.mark.parametrize("f, x0, x1, expected_root", [(F_QUADRATIC, 1.0, 2.0, SQRT2), (F_CUBIC, 1.0, 2.0, CBRT_OF_SHIFTED)])
    def test_converges_to_root(self, f: UnaryFunction, x0: Number, x1: Number, expected_root: Number) -> None:
        """Asserts that the secant method converges to the expected root within the tolerance."""

        *_, last = iter_secant(f, x0=x0, x1=x1, steps=SECANT_STEPS)

        assert abs(last - expected_root) < TOLERANCE

    def test_yields_at_most_n_steps(self) -> None:
        """Asserts that the secant method yields at most n estimates (may stop early on saturation)."""

        steps = 10
        estimates = list(iter_secant(F_QUADRATIC, x0=1.0, x1=1.5, steps=steps))

        assert len(estimates) <= steps

    def test_raises_zero_division_when_slope_is_zero(self) -> None:
        """Asserts that secant raises a ZeroDivisionError if the secant slope evaluates to zero before convergence."""

        with pytest.raises(ZeroDivisionError, match="slope is zero"):
            list(iter_secant(lambda x: 1.0, x0=1.0, x1=2.0, steps=5))


# -----------------------------------------------------------------------------
# iter_linear_iteration
# -----------------------------------------------------------------------------


class TestIterLinearIteration:
    def test_converges_to_fixed_point(self) -> None:
        """Asserts that the linear iteration method converges to the expected fixed point."""

        *_, last = iter_linear_iteration(PHI_SQRT2, x0=1.5, steps=STEPS)

        assert abs(last - SQRT2) < TOLERANCE

    def test_yields_exactly_n_steps(self) -> None:
        """Asserts that the linear iteration method yields exactly the requested number of estimates."""

        estimates = list(iter_linear_iteration(PHI_SQRT2, x0=1.5, steps=10))

        assert len(estimates) == 10
