from __future__ import annotations

from enum import Enum

from .number import Number


class Signal(Enum):
    """The arithmetic sign of a numeric value: positive, negative, or neutral."""

    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

    @classmethod
    def check_signal(cls, number: "Number") -> "Signal":
        """Returns the signal corresponding to the given number's sign."""
        if number == 0:
            return cls.NEUTRAL
        elif number < 0:
            return cls.NEGATIVE
        else:
            return cls.POSITIVE
