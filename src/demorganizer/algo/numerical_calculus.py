from math import ceil, log
from typing import Generator

from demorganizer.core import Interval, Number, UnaryFunction

# -----------------------------------------------------------------------------
# Bisection
# -----------------------------------------------------------------------------


def iter_bisection(f: "UnaryFunction", interval: Interval, steps: int) -> Generator[float, None, None]:
    """Yield successive midpoints from the bisection method for a fixed number of iterations.

    Repeatedly halves the interval [a, b] and selects the sub-interval
    where the sign change occurs, guaranteeing convergence to a root
    of f provided f(a) and f(b) have opposite signs.
    """

    a, b = interval

    y_a = f(a)
    y_b = f(b)

    if y_a * y_b > 0:
        raise ValueError("Interval endpoints must have opposite signs.")

    for _ in range(steps):
        x_mid = _calculate_bisection_midpoint(a, b)
        y_mid = f(x_mid)

        if y_a * y_mid < 0:
            b = x_mid
        else:
            a = x_mid
            y_a = y_mid

        yield x_mid


def calculate_bisection_steps(precision: float, interval: Interval) -> int:
    """Return the minimum number of bisection iterations to achieve the given precision.

    Derived from the bisection error bound: after n iterations the error
    is at most (b - a) / 2^n, so n > (log(b - a) - log(precision)) / log(2).
    """

    a, b = interval

    return ceil((log(b - a) - log(precision)) / log(2)) + 1


def _calculate_bisection_midpoint(a: Number, b: Number) -> Number:
    """Return the midpoint of interval [a, b]."""

    return (a + b) / 2.0


# -----------------------------------------------------------------------------
# False position
# -----------------------------------------------------------------------------


def iter_false_position(f: "UnaryFunction", interval: tuple[Number, Number], steps: int) -> Generator[float, None, None]:
    """Yield successive root estimates from the false-position method for a fixed number of iterations.

    Connects the points (a, f(a)) and (b, f(b)) with a secant line and
    takes its x-intercept as the next estimate, then narrows the interval
    around the sign change. Converges faster than bisection for smooth functions.
    """

    a, b = interval

    y_a = f(a)
    y_b = f(b)

    if y_a * y_b > 0:
        raise ValueError("Interval endpoints must have opposite signs.")

    for _ in range(steps):
        x_mid = _calculate_false_position_midpoint(a, b, y_a, y_b)
        y_mid = f(x_mid)

        if y_a * y_mid < 0:
            b = x_mid
        else:
            a = x_mid
            y_a = y_mid

        yield x_mid


def _calculate_false_position_midpoint(a: Number, b: Number, y_a: Number, y_b: Number) -> Number:
    """Return the false-position estimate of the root in interval [a, b]."""

    return ((a * y_b) - (b * y_a)) / (y_b - y_a)


# -----------------------------------------------------------------------------
# Linear iteration (fixed-point)
# -----------------------------------------------------------------------------


def iter_linear_iteration(phi: UnaryFunction, x0: Number, steps: int) -> Generator[float, None, None]:
    """Yield successive estimates from the fixed-point iteration x_{n+1} = phi(x_n).

    Given a function phi such that f(x) = 0 can be rewritten as x = phi(x),
    this method iterates from an initial guess toward a fixed point.
    """

    x = x0

    for _ in range(steps):
        x = phi(x)

        yield x


# -----------------------------------------------------------------------------
# Newton-Raphson
# -----------------------------------------------------------------------------


def iter_newton_raphson(f: UnaryFunction, df: UnaryFunction, x0: Number, steps: int) -> Generator[float, None, None]:
    """Yield successive root estimates from the Newton-Raphson method for a fixed number of iterations.

    At each step, linearises f around the current estimate using its
    derivative and computes the next estimate as x_{n+1} = x_n - f(x_n) / f'(x_n).
    Converges quadratically near simple roots when f'(x) ≠ 0.
    """

    x = x0

    for _ in range(steps):
        derivative = df(x)

        if derivative == 0:
            raise ZeroDivisionError("Derivative is zero; Newton-Raphson cannot continue.")

        x = x - (f(x) / derivative)

        yield x


# -----------------------------------------------------------------------------
# Secant
# -----------------------------------------------------------------------------


def iter_secant(f: UnaryFunction, x0: Number, x1: Number, steps: int) -> Generator[float, None, None]:
    """Yield successive root estimates from the secant method for a fixed number of iterations.

    Approximates the derivative of f using two previous points and computes
    the next estimate as the x-intercept of the secant line through
    (x_{n-1}, f(x_{n-1})) and (x_n, f(x_n)).  Converges super-linearly
    without requiring an explicit derivative function.
    """

    x_prev = x0
    x_curr = x1

    for _ in range(steps):
        f_prev = f(x_prev)
        f_curr = f(x_curr)

        denominator = f_curr - f_prev

        if denominator == 0:
            if x_prev == x_curr:
                return  # converged to machine precision; stop cleanly

            raise ZeroDivisionError("Secant slope is zero; method cannot continue.")

        x_next = x_curr - f_curr * (x_curr - x_prev) / denominator

        x_prev = x_curr
        x_curr = x_next

        yield x_curr
