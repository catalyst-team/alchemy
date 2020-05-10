import json
import os
import re
import unicodedata
from pathlib import Path
from typing import Union, Any

API_URL = "https://log.alchemy.host"
BASE_LOGS_DIR = "~/.alchemy/logs"

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


def dump_json(obj: Any, filename: Union[Path, str]):
    filename = Path(filename).expanduser().absolute()
    os.makedirs(filename.parent, exist_ok=True)
    with filename.open("w") as fp:
        json.dump(obj, fp)


def load_json(filename: Union[Path, str]) -> Any:
    with Path(filename).expanduser().absolute().open() as fp:
        return json.load(fp)


def is_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True
