from __future__ import annotations

from .expression import Expression


class Constant(Expression):
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


TRUE = Constant(True)
"""The boolean constant True (1)."""

FALSE = Constant(False)
"""The boolean constant False (0)."""
