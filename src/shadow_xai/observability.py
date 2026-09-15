"""Structured logging helpers without external dependencies."""

import json
import logging
import sys
from typing import Any


def configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(level=getattr(logging, level.upper(), logging.INFO), format="%(message)s", stream=sys.stderr)


def event(logger: logging.Logger, name: str, **fields: Any) -> None:
    payload = {"event": name, **fields}
    logger.info(json.dumps(payload, ensure_ascii=False, default=str))
