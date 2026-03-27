from math import ceil, log
from typing import TYPE_CHECKING, Generator

if TYPE_CHECKING:
    from demorganizer import algebra


def calculate_bisection_x(a: "algebra.Number", b: "algebra.Number") -> "algebra.Number":
    """Returns the midpoint of the interval [a, b]."""
    return (a + b) / 2


def find_required_bisection_steps(
    precision: float, interval: tuple["algebra.Number", "algebra.Number"]
) -> int:
    """Returns the number of iterations needed to reach the desired precision.

    Based on the bisection error bound: n > (log(b - a) - log(precision)) / log(2).
    """
    a, b = interval

    return ceil((log(b - a) - log(precision)) / log(2)) + 1


def apply_bisection_by_steps(
    f: "algebra.UnaryFunction",
    interval: tuple["algebra.Number", "algebra.Number"],
    steps: int,
) -> Generator[float, None, None]:
    """Runs the bisection method for a fixed number of iterations, yielding each midpoint."""
    a, b = interval
    y_a = f(a)
    y_b = f(b)

    if y_a * y_b > 0:
        raise ValueError("Interval endpoints must have opposite signs.")

    for _ in range(steps):
        x_mid = calculate_bisection_x(a, b)
        y_mid = f(x_mid)

        if y_a * y_mid < 0:
            b = x_mid
        else:
            a = x_mid
            y_a = y_mid

        yield x_mid


def apply_bisection_by_tolerance(
    f: "algebra.UnaryFunction",
    interval: tuple["algebra.Number", "algebra.Number"],
    precision: float,
) -> Generator[float, None, None]:
    """Finds the root by running bisection until the error tolerance is met."""
    steps = find_required_bisection_steps(precision, interval)

    return apply_bisection_by_steps(f, interval, steps)
