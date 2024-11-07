import datetime
import logging
import sys
import traceback
from enum import Enum
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from rich.console import Console
from zeeland import Singleton, get_default_storage_path


class Color(Enum):
    DEFAULT = "default"
    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"


class Logger(logging.Logger, metaclass=Singleton):
    """A custom logger class that extends logging.Logger with color output
    capabilities."""

    def __init__(self, name: str = "gcop", level: int = logging.DEBUG) -> None:
        """Initialize the logger with file and console handlers.

        Args:
            name: Logger name, defaults to "gcop"
            level: Logging level, defaults to DEBUG
        """
        super().__init__(name, level)
        self._setup_file_handler()
        self.console = Console()

    def _setup_file_handler(self) -> None:
        """Set up rotating file handler with formatting."""
        log_dir = Path(get_default_storage_path("gcop", "logs"))
        log_file = log_dir / f"{datetime.datetime.now().strftime('%Y%m%d')}.log"

        handler = TimedRotatingFileHandler(
            filename=log_file, when="midnight", interval=1, encoding="utf-8"
        )
        handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s:%(funcName)s:%(lineno)d - %(message)s",  # noqa
            "%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        self.addHandler(handler)

    def color_info(
        self, message: str, color: Color = Color.DEFAULT, *args, **kwargs
    ) -> None:
        """Log info message and print to console with optional color.

        Args:
            message: The message to log
            color: Color enum value for console output
            *args: Additional args passed to logger
            **kwargs: Additional kwargs passed to logger
        """
        self.info(message, *args, **kwargs)
        formatted_msg = (
            f"[{color.value}]{message}[/]" if color != Color.DEFAULT else message
        )
        self.console.print(formatted_msg, style=color.value)


def handle_exception(exc_type, exc_value, exc_tb) -> None:
    """Handle uncaught exceptions by logging them.

    Args:
        exc_type: Exception type
        exc_value: Exception value
        exc_tb: Exception traceback
    """
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_tb)
        return

    logger.error(
        "Uncaught exception:\n%s",
        "".join(traceback.format_exception(exc_type, exc_value, exc_tb)),
    )
    sys.__excepthook__(exc_type, exc_value, exc_tb)


logger = Logger()
sys.excepthook = handle_exception
