import time
import typing as t

from logging import Formatter, LogRecord, StreamHandler

from server.config import config
from server.const import DEFAULT_LOG_FORMAT, DEFAULT_LOG_FORMAT_DEV

if t.TYPE_CHECKING:
    from flask import Flask


def setup_logger(app: Flask) -> None:
    app.logger.setLevel(config.LOG_LEVEL)

    handler = next(
        (hd for hd in app.logger.handlers if isinstance(hd, StreamHandler)),
        None,
    )
    if handler is None:
        handler = StreamHandler()
        app.logger.addHandler(handler)

    handler.addFilter(_request_context_filter)

    format_str = _ditect_format(app)
    datefmt = config.LOG_DATEFMT
    formatter = Formatter(fmt=format_str, datefmt=datefmt)
    formatter.converter = time.gmtime
    handler.setFormatter(formatter)


def _ditect_format(app: Flask) -> str:
    if config.LOG_FORMAT is not None:
        return config.LOG_FORMAT

    if app.debug or app.config.get("ENV") == "development":
        return DEFAULT_LOG_FORMAT_DEV
    return DEFAULT_LOG_FORMAT


def _request_context_filter(record: LogRecord) -> bool:
    record.addr = "unknown"
    record.user = "anonymous"
    return True
