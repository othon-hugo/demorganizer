from typing import TYPE_CHECKING, Generator

if TYPE_CHECKING:
    from demorganizer import algebra


def calculate_false_position_x(
    a: "algebra.Number",
    b: "algebra.Number",
    y_a: "algebra.Number",
    y_b: "algebra.Number",
) -> "algebra.Number":
    """Returns the false-position estimate of the root within [a, b]."""
    return ((a * y_b) - (b * y_a)) / (y_b - y_a)


def apply_false_position_by_steps(
    f: "algebra.UnaryFunction",
    interval: tuple["algebra.Number", "algebra.Number"],
    steps: int,
) -> Generator[float, None, None]:
    """Runs the false-position method for a fixed number of iterations, yielding each estimate."""
    a, b = interval

    y_a = f(a)
    y_b = f(b)

    if y_a * y_b > 0:
        raise ValueError("Interval endpoints must have opposite signs.")

    for _ in range(steps):
        x_mid = calculate_false_position_x(a, b, y_a, y_b)
        y_mid = f(x_mid)

        if y_a * y_mid < 0:
            b = x_mid
        else:
            a = x_mid
            y_a = y_mid

        yield x_mid
