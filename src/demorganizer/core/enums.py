from enum import Enum
from typing import TYPE_CHECKING
from typing_extensions import Self

if TYPE_CHECKING:
    from demorganizer.core import Number


class Signal(Enum):
    """The arithmetic sign of a numeric value: positive, negative, or neutral."""

    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
