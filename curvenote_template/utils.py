import logging


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
