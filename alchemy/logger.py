import logging
import os
import uuid
from collections import Counter
from pathlib import Path
from typing import Union

from .sender import Sender
from .utils import validate, dump_json, validate_metric, BASE_LOGS_DIR


class Logger:
    _base_logs_dir = BASE_LOGS_DIR

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
        dump_json({
            "X-Token": self._token,
            "X-Project": self._project,
            "X-Group": self._group,
            "X-Experiment": self._experiment,
        }, self._logs_dir / "headers.json")

    @property
    def _batch_filename(self):
        filename = "%09d" % self._batch_no + ".json"
        filename = self._logs_dir / "logs" / filename
        self._batch_no += 1
        return filename

    def _dump_batch(self):
        if len(self._batch):
            fn = str(self._batch_filename)
            dump_json(self._batch, fn + "_")
            os.rename(fn + "_", fn)
            self._batch = []
            logging.debug(f"dump batch: {fn}")

    def close(self):
        self._dump_batch()

    def log_scalar(self, name: str, value: Union[int, float]):
        self._batch.append(dict(
            name=validate_metric(name, f"invalid metric name: {name}"),
            value=value,
            step=self._counters[name],
        ))
        self._counters[name] += 1
        if len(self._batch) >= self._batch_size:
            self._dump_batch()
