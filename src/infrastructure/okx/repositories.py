from __future__ import annotations

from infrastructure.common import WebSocketPriceFeedRepository

from .client import OkxClientConfig, OkxWebSocketClient


class OkxPriceFeedRepository(WebSocketPriceFeedRepository[OkxClientConfig]):
    client_cls = OkxWebSocketClient

    def __init__(self, contract_type: str | None = None) -> None:
        super().__init__(contract_type)

    def _build_config(self, contract_type: str | None) -> OkxClientConfig:
        default_inst_type = contract_type.upper() if contract_type else None
        return OkxClientConfig(default_inst_type=default_inst_type)
