from math import ceil, log
from typing import Generator

from demorganizer.core import Interval, Number, UnaryFunction

# --- Bisection ----


def iter_bisection_by_steps(f: "UnaryFunction", interval: Interval, steps: int) -> Generator[float, None, None]:
    """Yield successive midpoints from the bisection method for a fixed number of iterations."""

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


def iter_bisection_by_tolerance(f: "UnaryFunction", interval: Interval, precision: float) -> Generator[float, None, None]:
    """Yield successive midpoints from the bisection method until the desired tolerance is reached."""

    steps = _calculate_bisection_steps(precision, interval)

    return iter_bisection_by_steps(f, interval, steps)


def _calculate_bisection_steps(precision: float, interval: Interval) -> int:
    """Return the minimum number of bisection iterations to achieve the given precision.

    Based on the bisection error bound:
        n > (log(b - a) - log(precision)) / log(2).
    """

    a, b = interval

    return ceil((log(b - a) - log(precision)) / log(2)) + 1


def _calculate_bisection_midpoint(a: Number, b: Number) -> Number:
    """Return the midpoint of interval [a, b]."""

    return (a + b) / 2.0


# --- False position ----


def iter_false_position_by_steps(f: "UnaryFunction", interval: tuple[Number, Number], steps: int) -> Generator[float, None, None]:
    """Yield successive root estimates from the false-position method for a fixed number of iterations."""
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
