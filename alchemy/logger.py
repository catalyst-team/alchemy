from typing import Union
from collections import Counter
import logging
import os
from pathlib import Path
import uuid

from .sender import Sender
from .utils import BASE_LOGS_DIR, dump_json, validate, validate_metric


class Logger:
    """
    Logging experiments data to disk.
    """

    _base_logs_dir = BASE_LOGS_DIR

    def __init__(
        self,
        token: str,
        experiment: str,
        group: str = None,
        project: str = None,
        batch_size: int = None,
    ):
        """
        Args:
            token: corresponds for specific workspace, get it in your
                   profile (web ui). Required.
            experiment: name of experiment. Required.
            group: name of group. Default is 'default'.
            project: name of project. Default is 'default'.
            batch_size: size of batch to send. Default is 1000.
        """
        self._token = token
        self._experiment = validate(
            experiment, f"invalid experiment name: {experiment}"
        )
        group = group or "default"
        self._group = validate(group, f"invalid group name: {group}")
        project = project or "default"
        self._project = validate(project, f"invalid project name: {project}")
        base_logs_dir = Path(self._base_logs_dir).expanduser().absolute()
        self._logs_dir: Path = base_logs_dir / str(uuid.uuid4())
        self._batch_size = max(int(batch_size or int(1e3)), 1)
        self._counters = Counter()
        self._batch = []
        self._batch_no = 0
        self._dump_headers()
        self._dump_pid()
        self._run_sender()

    def _run_sender(self):
        Sender(self._logs_dir).run_daemon()

    def _dump_pid(self):
        dump_json({"pid": os.getpid()}, self._logs_dir / "pid.json")

    def _dump_headers(self):
        dump_json(
            {
                "X-Token": self._token,
                "X-Project": self._project,
                "X-Group": self._group,
                "X-Experiment": self._experiment,
            },
            self._logs_dir / "headers.json",
        )

    @property
    def _batch_filename(self):
        filename = "%09d" % self._batch_no + ".json"
        filename = self._logs_dir / "logs" / filename
        self._batch_no += 1
        return filename

    def _dump_batch(self):
        if self._batch:
            dump_json(self._batch, self._batch_filename)
            self._batch = []
            logging.debug(f"dump batch: {self._batch_filename}")

    def close(self):
        """
        This method flushes last batch to the disk.

        Returns: None
        """
        self._dump_batch()

    def log_scalar(
        self, name: str, value: Union[int, float], step: int = None,
    ):
        """
        Log some scalar metric.

        Args:
            name: metric name. Required.
            value: metric value. Required.
            step: Default is None (autoincrement starting from 1).

        Returns: None
        """
        self._batch.append(
            {
                "name": validate_metric(name, f"invalid metric name: {name}"),
                "value": value,
                "step": step or self._counters[name],
            }
        )
        self._counters[name] += 1
        if len(self._batch) >= self._batch_size:
            self._dump_batch()
