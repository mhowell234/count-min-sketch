from abc import ABCMeta, abstractmethod
from typing import Any


class CountMinSketch(metaclass=ABCMeta):

    @abstractmethod
    def add(self, item: Any) -> None:
        """Adds an item to the sketch

        Args:
            item: item to add
        """

    @abstractmethod
    def estimate(self, item: Any) -> int:
        """Returns the floor of the number of times this item has been inserted. May overestimate; never underestimate.

        Returns:
            The floor of how many times this item has been inserted
        """

    @abstractmethod
    def remove(self, item: Any, times: int = 1) -> None:
        """Removes an item N times

        Args:
            item: item
            times: number of times to remove
        """
