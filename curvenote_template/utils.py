import logging
import requests


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