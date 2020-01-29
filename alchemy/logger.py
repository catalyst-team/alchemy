import queue
import threading
from collections import Counter
from typing import Union

import requests


class Logger:
    _url = "https://alchemy.host/api/log"

    def __init__(
            self,
            token: str,
            experiment: str,
            group: str = None,
            project: str = None,
            batch_size: int = None,
    ):
        self._token = token
        self._experiment = experiment
        self._group = group or "default"
        self._project = project or "default"
        self._batch_size = batch_size or int(1e3)
        self._counters = Counter()
        self._queue = queue.Queue()
        self._thread = threading.Thread(target=self._run_worker)
        self._thread.start()

    def _run_worker(self):
        headers = {
            'X-Token': self._token,
            'X-Project': self._project,
            'X-Group': self._group,
            'X-Experiment': self._experiment,
        }
        running = True
        while running:
            batch = []
            try:
                while len(batch) < self._batch_size:
                    if batch:
                        msg = self._queue.get_nowait()
                    else:
                        msg = self._queue.get()
                    if msg is None:
                        running = False
                        break
                    batch.append(msg)
            except queue.Empty:
                pass
            if batch:
                requests.post(self._url, json=batch, headers=headers)

    def close(self):
        if not self._thread.is_alive():
            return
        self._queue.put(None)
        self._thread.join()

    def log_scalar(
            self,
            name: str,
            value: Union[int, float],
    ):
        self._queue.put(dict(
            name=name,
            value=value,
            step=self._counters[name],
        ))
        self._counters[name] += 1
