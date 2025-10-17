from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Final

from dotenv import load_dotenv

from logging_config import configure_logging

load_dotenv()
configure_logging()


def _get_env(name: str) -> str | None:
    value = os.getenv(name)
    return value.strip() if value is not None else None


def _get_float(name: str, default: float) -> float:
    raw = _get_env(name)
    if raw is None:
        return default
    try:
        return float(raw)
    except ValueError as exc:  # noqa: TRY003 - propagate config errors clearly
        raise ValueError(f"Environment variable {name} must be a float") from exc


def _get_int(name: str, default: int) -> int:
    raw = _get_env(name)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError as exc:  # noqa: TRY003 - propagate config errors clearly
        raise ValueError(f"Environment variable {name} must be an integer") from exc


def _get_str(name: str, default: str) -> str:
    raw = _get_env(name)
    return raw if raw is not None else default


@dataclass(frozen=True)
class ConnectorSettings:
    inactivity_timeout: float
    reconnect_delay: float
    rest_timeout: float
    ws_ping_interval: float
    ws_ping_timeout: float
    stream_idle_timeout: float
    max_symbol_per_ws: int


@dataclass(frozen=True)
class WsServerSettings:
    host: str
    port: int
    log_level: str
    subscribe_timeout: float


@dataclass(frozen=True)
class Settings:
    connector: ConnectorSettings
    ws_server: WsServerSettings


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    connector = ConnectorSettings(
        inactivity_timeout=_get_float("CONNECTOR_INACTIVITY_TIMEOUT", 3.0),
        reconnect_delay=_get_float("CONNECTOR_RECONNECT_DELAY", 1.0),
        rest_timeout=_get_float("CONNECTOR_REST_TIMEOUT", 5.0),
        ws_ping_interval=_get_float("CONNECTOR_WS_PING_INTERVAL", 20.0),
        ws_ping_timeout=_get_float("CONNECTOR_WS_PING_TIMEOUT", 20.0),
        stream_idle_timeout=_get_float("CONNECTOR_STREAM_IDLE_TIMEOUT", 10.0),
        max_symbol_per_ws=_get_int("CONNECTOR_MAX_SYMBOL_PER_WS", 50),
    )

    ws_server = WsServerSettings(
        host=_get_str("CONNECTOR_WSS_HOST", "0.0.0.0"),
        port=_get_int("CONNECTOR_WSS_PORT", 8765),
        log_level=_get_str("CONNECTOR_WSS_LOG_LEVEL", "INFO"),
        subscribe_timeout=_get_float("CONNECTOR_WSS_SUBSCRIBE_TIMEOUT", 10.0),
    )

    return Settings(connector=connector, ws_server=ws_server)


SETTINGS: Final[Settings] = get_settings()
