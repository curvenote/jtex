import logging
from typing import Dict, Optional, Tuple

import requests
import yaml


def just_log_errors(message_func):
    """
    creates a decorator to allow us to eat errors and continue
    while providing a custom log message
    """

    def decorator(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValueError:
                logging.info(message_func(*args, **kwargs))

        return inner

    return decorator


def log_and_raise_errors(message_func):
    """
    creates a decorator to allow us to eat errors and continue
    while providing a custom log message
    """

    def decorator(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValueError as err:
                logging.error(message_func(*args, **kwargs))
                logging.error("Error: %s", str(err))
                raise err

        return inner

    return decorator


def download(url, save_path, chunk_size=128):
    """
    Download a file from a url and save to the save_path provided
    """
    resp = requests.get(url, stream=True)
    with open(save_path, "wb") as file:
        for chunk in resp.iter_content(chunk_size=chunk_size):
            file.write(chunk)


FM_DELIM = "% ---"
FM_LINE = "% "


def parse_front_matter(content: str) -> Tuple[Optional[Dict], str]:
    if len(content) == 0 or content.count(FM_DELIM) < 2:
        return None, ""

    lines = content.split("\n")
    fm_lines = []
    collect = False
    idx = 0
    for line in lines:
        idx += 1
        if line.startswith(FM_DELIM):
            if not collect:
                collect = True
                continue
            else:
                break
        if collect:
            fm_lines.append(line[len(FM_LINE) :])

    rest = "\n".join(lines[idx:])

    return (
        yaml.load("\n".join(fm_lines), Loader=yaml.FullLoader),
        rest if len(rest) > 0 else "",
    )


def stringify_front_matter(data: Dict):
    if len(data.keys()) == 0:
        return ""

    raw_fm = yaml.dump(data)
    lines = raw_fm.split("\n")

    front_matter_lines = [f"{FM_DELIM}"]
    for line in lines:
        if len(line) == 0:
            continue
        front_matter_lines.append(f"{FM_LINE}{line}")
    front_matter_lines.append(f"{FM_DELIM}")

    front_matter_section = "\n".join(front_matter_lines)
    return f"{front_matter_section}\n"
