#!/usr/bin/env python3
"""
A small web service for printing similar words in the English language.
"""
import datetime
import json
import sys
from collections import defaultdict

__author__ = "Roy Moore"
__license__ = "MIT"
__version__ = "1.0.0"

import argparse
import logging

from flask import Flask, request

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%H:%M:%S',
                    handlers=[logging.StreamHandler(sys.stdout)]
                    )

log = logging.getLogger(__name__)

app = Flask(__name__)

BASE_URL = "/api/"
VERSION_URL = BASE_URL + 'v1/'
PING_URL = VERSION_URL + 'ping'
SIMILAR_URL = VERSION_URL + 'similar'
STATS_URL = VERSION_URL + 'stats'

DataBase = dict()


@app.route(PING_URL, methods=['GET'])
def get_test():
    return "pong"


@app.route(SIMILAR_URL, methods=['GET'])
def get_similar():
    global DataBase

    requested_word = request.args.get('word')
    result = DataBase[_sort_word(requested_word)]
    result.remove(requested_word)

    return json.dumps(result)


@app.route(STATS_URL, methods=['GET'])
def get_stats():
    return "stats"


def _sort_word(word):
    """
    Used to return a sorted string based on a given word
    :param str word:
    :rtype: str
    """
    return "".join((sorted(word)))


def load_data_file(path):
    """
    :param str path: path of DB (English dictionary)
    """
    global DataBase
    start_time = datetime.datetime.now()
    loaded_db = defaultdict(list)
    words = 0

    with open(path, "r") as fileHandler:
        for line in fileHandler:
            words += 1
            word = line.strip()  # Need to stripe as each line (except last one) will contain new line character
            sorted_word = _sort_word(word)  # get the sorted version of the word
            loaded_db[sorted_word] += [word]  # Insert the data to the DB

    DataBase = loaded_db

    end_time = datetime.datetime.now()
    log.info(f"DB loaded successfully (load time = {(end_time - start_time).total_seconds()} seconds)")
    log.debug(f"Words count = {words}, "
              f"DB Keys = {len(loaded_db.keys())}, "
              f"DB Values = {sum([len(loaded_db[x]) for x in loaded_db if isinstance(loaded_db[x], list)])}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Print Similar Web Service')
    parser.add_argument("-d", "--debug", action="store_true", default=False, help="enable debug mode")
    parser.add_argument("-n", "--host", action="store", type=str, default="0.0.0.0", help="hostname to listen on")
    parser.add_argument("-p", "--port", action="store", type=int, default=8000, help="port of the webserver")
    parser.add_argument("-f", "--file", action="store", type=str, default="words_clean.txt", help="source data file")
    args = parser.parse_args()

    load_data_file(args.file)

    app.run(debug=args.debug, host=args.host, port=args.port)
