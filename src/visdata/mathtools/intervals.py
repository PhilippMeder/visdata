from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class BaseInterval(ABC):
    """Abstract base class for intervals."""

    left: Any
    right: Any

    @abstractmethod
    def __contains__(self, test_obj):
        """Check if 'test_obj' is in the interval range."""

    @abstractmethod
    def __str__(self):
        """Return a human-readable interval representation."""

    def __iter__(self):
        """Make interval iterable over boundaries (allows min(), max())."""
        yield self.left
        yield self.right

    @property
    @abstractmethod
    def closed_left(self) -> bool:
        """Return left closed status of interval."""

    @property
    @abstractmethod
    def closed_right(self) -> bool:
        """Return right closed status of interval."""

    def __post_init__(self):
        """Check if interval is reasonable."""
        if not self.left <= self.right:
            raise ValueError(
                f"Wrong boundaries! {self} has a left boundary bigger than the"
                " right!"
            )

    @property
    def closed(self) -> bool:
        """Return wether interval is completely closed or not."""
        return self.closed_left and self.closed_right

    @property
    def half_open(self) -> bool:
        """Return wether interval is a half-open interval or not."""
        return self.closed_left != self.closed_right

    @property
    def opened(self) -> bool:
        """Return wether interval is completely open or not."""
        return self.open_right and self.open_left

    @property
    def open_left(self) -> bool:
        """Return left open status of interval."""
        return not self.closed_left

    @property
    def open_right(self) -> bool:
        """Return right open status of interval."""
        return not self.closed_right

    @property
    def midpoint(self):
        return (self.left + self.right) / 2


class OpenInterval(BaseInterval):
    """Open interval (a, b)."""

    def __contains__(self, test_obj):
        """Check if 'test_obj' is in the interval range."""
        return self.left < test_obj and test_obj < self.right

    def __str__(self):
        """Return a human-readable interval representation."""
        return f"({self.left}, {self.right})"

    @property
    def closed_left(self) -> bool:
        """Return left closed status of interval."""
        return False

    @property
    def closed_right(self) -> bool:
        """Return right closed status of interval."""
        return False


class RightOpenInterval(BaseInterval):
    """Right-open interval [a, b)."""

    def __contains__(self, test_obj):
        """Check if 'test_obj' is in the interval range."""
        return self.left <= test_obj and test_obj < self.right

    def __str__(self):
        """Return a human-readable interval representation."""
        return f"[{self.left}, {self.right})"

    @property
    def closed_left(self) -> bool:
        """Return left closed status of interval."""
        return True

    @property
    def closed_right(self) -> bool:
        """Return right closed status of interval."""
        return False


class LeftOpenInterval(BaseInterval):
    """Left-open interval (a, b]."""

    def __contains__(self, test_obj):
        """Check if 'test_obj' is in the interval range."""
        return self.left < test_obj and test_obj <= self.right

    def __str__(self):
        """Return a human-readable interval representation."""
        return f"({self.left}, {self.right}]"

    @property
    def closed_left(self) -> bool:
        """Return left closed status of interval."""
        return False

    @property
    def closed_right(self) -> bool:
        """Return right closed status of interval."""
        return True


class ClosedInterval(BaseInterval):
    """Closed interval [a, b]."""

    def __contains__(self, test_obj):
        """Check if 'test_obj' is in the interval range."""
        return self.left <= test_obj and test_obj <= self.right

    def __str__(self):
        """Return a human-readable interval representation."""
        return f"[{self.left}, {self.right}]"

    @property
    def closed_left(self) -> bool:
        """Return left closed status of interval."""
        return True

    @property
    def closed_right(self) -> bool:
        """Return right closed status of interval."""
        return True


class Interval:

    def __new__(cls, left, right, closed=None):
        """Wrapper which selects the interval type with 'closed' argument."""
        match closed:
            case "both" | "b" | True:
                interval_class = ClosedInterval
            case "left" | "l":
                interval_class = RightOpenInterval
            case "right" | "r":
                interval_class = LeftOpenInterval
            case "not" | "neither" | "n" | False | None:
                interval_class = OpenInterval
            case _:
                raise ValueError(f"Unexpected value '{closed}' for 'closed'!")

        return interval_class(left, right)
