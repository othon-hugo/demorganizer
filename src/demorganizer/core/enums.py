from enum import Enum


class Signal(Enum):
    """The arithmetic sign of a numeric value: positive, negative, or neutral."""

    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
