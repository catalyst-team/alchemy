from typing import Union
import logging
from multiprocessing import Process
from pathlib import Path
import shutil
import time

import daemon
from filelock import FileLock
import requests

from .utils import API_URL, is_alive, load_json


class Sender:
    """
    Send logs to alchemy backend.
    """

    _url = API_URL

    def __init__(self, logs_dir: Union[Path, str]):
        """
        Args:
            logs_dir: directory with experiment logs
        """
        self._logs_dir: Path = Path(logs_dir).expanduser().absolute()

    def run_daemon(self):
        """
        Send logs to alchemy backend (daemon mode).

        Returns: None
        """
        proc = Process(target=self._run, name="alchemy-sender",)
        proc.start()
        proc.join()

    def _run(self):
        log = (self._logs_dir / "sender.log").open("w+")
        with daemon.DaemonContext(detach_process=True, stderr=log, stdout=log):
            self.run()

    def run(self):
        """
        Send logs to alchemy backend.

        Returns: None
        """
        lock_filename = self._logs_dir / ".lock"
        lock = FileLock(lock_filename, timeout=10)
        with lock:
            pid = load_json(self._logs_dir / "pid.json")["pid"]
            headers = load_json(self._logs_dir / "headers.json")
            logs = self._logs_dir / "logs"
            while True:
                batches = list(logs.glob("*.json"))
                if not batches:
                    if is_alive(pid):
                        time.sleep(10)
                        continue
                    else:
                        break

                batches.sort()
                for batch_filename in batches:
                    batch = load_json(batch_filename)
                    try:
                        logging.debug(f"send batch: {batch_filename}")
                        requests.post(self._url, json=batch, headers=headers)
                        batch_filename.unlink()
                    except Exception as e:
                        logging.exception(e)
                        time.sleep(30)
                        break
            logging.debug(f"delete logs: {self._logs_dir}")
            shutil.rmtree(self._logs_dir, ignore_errors=True)
