from typing import Callable, Tuple, TypeAlias

Number: TypeAlias = int | float
"""A real numeric scalar, either integer or floating-point."""


UnaryFunction: TypeAlias = Callable[[Number], Number]
"""A function that maps a single numeric value to another numeric value."""

Interval: TypeAlias = Tuple[Number, Number]
"""..."""
