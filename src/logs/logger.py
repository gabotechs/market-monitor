import logging

import coloredlogs

log = None


def _get(level: str = "INFO") -> logging.Logger:
    global log
    if not log:
        log = logging.getLogger()
        log.setLevel(logging.__dict__[level.upper()])
        coloredlogs.install(logger=log)
        log.propagate = False

    return log


def debug(msg, *args, **kwargs):
    _get().debug(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    _get().info(msg, *args, **kwargs)


def warning(msg, *args, **kwargs):
    _get().warning(msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    _get().error(msg, *args, **kwargs)
