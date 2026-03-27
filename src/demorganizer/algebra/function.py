from typing import Callable, TypeAlias

from .number import Number

UnaryFunction: TypeAlias = Callable[["Number"], "Number"]
"""A function that maps a single numeric value to another numeric value."""
