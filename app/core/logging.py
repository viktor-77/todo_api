import logging
import sys


def configure_logging(level: str = "INFO") -> None:
    """
    Configure simple, production-friendly logging.
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        stream=sys.stdout,
    )
    logging.getLogger("uvicorn.error").setLevel(level)
    logging.getLogger("uvicorn.access").setLevel(level)
    logging.getLogger("pymongo").setLevel("WARNING")
