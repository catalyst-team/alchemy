from typing import Any, Union
import json
import os
from pathlib import Path
import re
import unicodedata

API_URL = "https://log.alchemy.host"
BASE_LOGS_DIR = "~/.alchemy/logs"

VALID_MASK = r"^[a-zA-Z0-9_\-]{3,64}$"
VALID_RE = re.compile(VALID_MASK)

VALID_METRIC_MASK = r"^[\w\-/]{3,64}$"
VALID_METRIC_RE = re.compile(VALID_METRIC_MASK)


def validate(name: str, reason: str, error_type: type = ValueError):
    """
    Validate experiment/group/project name.

    Args:
        name: name to validate
        reason: error prefix (if name is invalid)
        error_type: base exception class to raise in case of validation error

    Returns: original name or raise error
    """
    if VALID_RE.match(name):
        return name
    raise error_type(f"{reason} (no match: {VALID_MASK})")


def validate_metric(name: str, reason: str, error_type: type = ValueError):
    """
    Validate metric name.

    Args:
        name: name to validate
        reason: error prefix (if name is invalid)
        error_type: base exception class to raise in case of validation error

    Returns: original name or raise error
    """
    name = unicodedata.normalize("NFKC", name)
    if VALID_METRIC_RE.match(name):
        return name
    raise error_type(f"{reason} (no match: {VALID_METRIC_MASK})")


def dump_json(obj: Any, filename: Union[Path, str]):
    """
    Dump json to file (atomic).

    Args:
        obj: object to dump
        filename: name of file

    Returns: None
    """
    tmp = Path(str(filename) + "_").expanduser().absolute()
    filename = Path(filename).expanduser().absolute()
    os.makedirs(filename.parent, exist_ok=True)
    with tmp.open("w") as fp:
        json.dump(obj, fp)
    os.rename(tmp, filename)


def load_json(filename: Union[Path, str]) -> Any:
    """
    Load json from file.

    Args:
        filename: name of file

    Returns: deserialized json
    """
    with Path(filename).expanduser().absolute().open() as fp:
        return json.load(fp)


def is_alive(pid: int) -> bool:
    """
    Check if process with target PID exists.
    Args:
        pid: PID of process

    Returns: True if process exists, False otherwise
    """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True
