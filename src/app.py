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

# noinspection SpellCheckingInspection
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%H:%M:%S',
                    handlers=[logging.StreamHandler(sys.stdout)])


class FancyDictionary:
    def __init__(self, path, logger):
        """
        :param str path: path of DB (English dictionary)
        """
        self.logger = logger
        self._data = self._load_data_file(path)

    @staticmethod
    def _sort_word(word):
        """
        Used to return a sorted string based on a given word
        :param str word:
        :rtype: str
        """
        return "".join((sorted(word)))

    def check(self, word):
        """
        Fetch a word from the DB
        :param str word:
        :rtype: list[str]
        """
        search_item = self._sort_word(word)
        result = self._data[search_item].copy()
        result.remove(word)

        return result

    def _load_data_file(self, path):
        """
        Load a txt file to a local dictionary DB
        :param str path: path of DB (English dictionary)
        """
        start_time = datetime.datetime.now()
        data = defaultdict(list)
        words = 0

        with open(path, "r") as fileHandler:
            for line in fileHandler:
                words += 1
                word = line.strip()  # Need to stripe as each line (except last one) will contain new line character
                sorted_word = self._sort_word(word)  # get the sorted version of the word
                data[sorted_word] += [word]  # Insert the data to the DB

        end_time = datetime.datetime.now()

        self.logger.info(f"DB loaded successfully (load time = {(end_time - start_time).total_seconds()} seconds)")
        self.logger.debug(f"Words count = {words}, "
                          f"DB Keys = {len(data.keys())}, "
                          f"DB Values = {sum([len(data[x]) for x in data if isinstance(data[x], list)])}")

        return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Print Similar Web Service')
    parser.add_argument("-d", "--debug", action="store_true", default=False, help="enable debug mode")
    parser.add_argument("-n", "--host", action="store", type=str, default="0.0.0.0", help="hostname to listen on")
    parser.add_argument("-p", "--port", action="store", type=int, default=8000, help="port of the webserver")
    parser.add_argument("-f", "--file", action="store", type=str, default="words_clean.txt", help="source data file")
    args = parser.parse_args()

    log = logging.getLogger(__name__)

    DB = FancyDictionary(args.file, log)

    app = Flask(__name__)

    BASE_URL = "/api/"
    VERSION_URL = BASE_URL + 'v1/'
    PING_URL = VERSION_URL + 'ping'
    SIMILAR_URL = VERSION_URL + 'similar'
    STATS_URL = VERSION_URL + 'stats'


    @app.route(PING_URL, methods=['GET'])
    def get_test():
        return "pong"


    @app.route(SIMILAR_URL, methods=['GET'])
    def get_similar():
        requested_word = request.args.get('word')
        found = DB.check(requested_word)

        return json.dumps(found)


    @app.route(STATS_URL, methods=['GET'])
    def get_stats():
        return "stats"

    app.run(debug=args.debug, host=args.host, port=args.port)
