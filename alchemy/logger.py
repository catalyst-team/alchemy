from collections import Counter
import queue
import re
import threading
from typing import Union
import unicodedata

import requests

VALID_MASK = r"^[a-zA-Z0-9_\-]{3,64}$"
VALID_RE = re.compile(VALID_MASK)

VALID_METRIC_MASK = r"^[\w\-/]{3,64}$"
VALID_METRIC_RE = re.compile(VALID_METRIC_MASK)


def validate(name: str, reason: str, error_type: type = ValueError):
    if VALID_RE.match(name):
        return name
    raise error_type(f"{reason} (no match: {VALID_MASK})")


def validate_metric(name: str, reason: str, error_type: type = ValueError):
    name = unicodedata.normalize("NFKC", name)
    if VALID_METRIC_RE.match(name):
        return name
    raise error_type(f"{reason} (no match: {VALID_METRIC_MASK})")


class Logger:
    _url = "https://log.alchemy.host"

    def __init__(
        self,
        token: str,
        experiment: str,
        group: str = None,
        project: str = None,
        batch_size: int = None,
    ):
        self._token = token
        self._experiment = validate(
            experiment, f"invalid experiment name: {experiment}"
        )
        group = group or "default"
        self._group = validate(group, f"invalid group name: {group}")
        project = project or "default"
        self._project = validate(project, f"invalid project name: {project}")
        self._batch_size = max(int(batch_size or int(1e3)), 1)
        self._counters = Counter()
        self._queue = queue.Queue()
        self._thread = threading.Thread(target=self._run_worker)
        self._thread.start()

    def _run_worker(self):
        headers = {
            "X-Token": self._token,
            "X-Project": self._project,
            "X-Group": self._group,
            "X-Experiment": self._experiment,
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
        step: int = None,
    ):
        self._queue.put(
            dict(
                name=validate_metric(name, f"invalid metric name: {name}"),
                value=value,
                step=step or self._counters[name],
            )
        )
        self._counters[name] += 1
