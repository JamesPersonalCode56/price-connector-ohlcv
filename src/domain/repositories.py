from abc import ABC, abstractmethod
from typing import AsyncIterator, Iterable

from .models import PriceQuote


class PriceFeedRepository(ABC):
    """Abstract gateway for streaming quotes from an exchange or market."""

    @abstractmethod
    def stream_quotes(self, symbols: Iterable[str]) -> AsyncIterator[PriceQuote]:
        """Return an async iterator yielding `PriceQuote` objects."""
        raise NotImplementedError
