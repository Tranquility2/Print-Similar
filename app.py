#!/usr/bin/env python3
"""
A small web service for printing similar words in the English language.
"""
import datetime
import sys
from collections import defaultdict

__author__ = "Roy Moore"
__license__ = "MIT"
__version__ = "1.0.0"

import argparse
import logging

from flask import Flask

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%H:%M:%S',
                    handlers=[logging.StreamHandler(sys.stdout)]
                    )

log = logging.getLogger(__name__)

app = Flask(__name__)


@app.route('/')
def index():
    return "Test"


def load_data_file(path):
    """
    :param str path: path of DB (English dictionary)
    :rtype: dict
    """
    start_time = datetime.datetime.now()
    db = defaultdict(list)
    # Open file
    with open(path, "r") as fileHandler:
        # Read each line in loop
        for line in fileHandler:
            # As each line (except last one) will contain new line character, so strip that
            word = line.strip()
            sorted_word = "".join((sorted(word)))
            db[sorted_word] += [word]

    end_time = datetime.datetime.now()

    log.info(f"DB load time = {(end_time-start_time).total_seconds()} seconds")

    return db


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Print Similar Web Service')
    parser.add_argument("-d", "--debug", action="store_true", default=False, help="enable debug mode")
    parser.add_argument("-n", "--host", action="store", type=str, default="0.0.0.0", help="hostname to listen on")
    parser.add_argument("-p", "--port", action="store", type=int, default=8000, help="port of the webserver")
    parser.add_argument("-f", "--file", action="store", type=str, default="words_clean.txt", help="source data file")
    args = parser.parse_args()

    db = load_data_file(args.file)

    app.run(debug=args.debug, host=args.host, port=args.port)
