import argparse
import logging
from pathlib import Path
from typing import Union

from .sender import Sender
from .utils import BASE_LOGS_DIR


def sync(logs_dir: Union[Path, str]):
    logs_dir = Path(logs_dir).expanduser().absolute()
    for log_dir in logs_dir.glob("*"):
        logging.info(f"send logs: {log_dir}")
        Sender(logs_dir=log_dir).run()


def main():
    parser = argparse.ArgumentParser("alchemy", description="Alchemy Tools")
    parser.add_argument("command", choices=["sync"])
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    if args.command == "sync":
        sync(BASE_LOGS_DIR)


main()
