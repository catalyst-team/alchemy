from typing import Union
import argparse
import logging
from pathlib import Path

from .sender import Sender
from .utils import BASE_LOGS_DIR


def sync(logs_dir: Union[Path, str]):
    """
    Send logs for all the experiments to alchemy backend.

    Args:
        logs_dir: base directory with logs.

    Returns: None
    """
    logs_dir = Path(logs_dir).expanduser().absolute()
    for log_dir in logs_dir.glob("*"):
        logging.info(f"send logs: {log_dir}")
        Sender(logs_dir=log_dir).run()


def main():  # noqa: D103
    parser = argparse.ArgumentParser("alchemy", description="Alchemy Tools")
    parser.add_argument("command", choices=["sync"])
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    if args.command == "sync":
        sync(BASE_LOGS_DIR)


main()
