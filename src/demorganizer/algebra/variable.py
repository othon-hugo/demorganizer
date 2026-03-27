from __future__ import annotations

from .expression import Expression


class Variable(Expression):
    """A boolean expression representing a named, single-character variable."""

    def __init__(self, name: str):
        """Initializes the variable, raising ValueError if name is not a single letter."""
        if not name.isalpha() or len(name) != 1:
            raise ValueError("Variable name must be a single alphabetic character.")

        self.name = name

    def __str__(self) -> str:
        """Returns the variable's single-character name."""
        return self.name

    @property
    def variables(self) -> set[str]:
        """Returns a set containing only this variable's name."""
        return {self.name}

    def evaluate(self, bindings: dict[str, bool]) -> bool:
        """Returns the value bound to this variable's name, raising ValueError if absent."""
        if self.name not in bindings:
            raise ValueError(f"Missing binding for variable: {self.name!r}")

        return bindings[self.name]
