from typing import AsyncIterator, Iterable

from domain.models import PriceQuote
from domain.repositories import PriceFeedRepository


class StreamPrices:
    """Use case to expose a streaming interface for market quotes."""

    def __init__(self, repository: PriceFeedRepository) -> None:
        self._repository = repository

    def execute(self, symbols: Iterable[str]) -> AsyncIterator[PriceQuote]:
        return self._repository.stream_quotes(symbols)
