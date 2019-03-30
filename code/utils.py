"""
Utils for Print Similar web service
"""
import logging


def config_logs(name, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    formatter.datefmt = '%H:%M:%S'
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger
