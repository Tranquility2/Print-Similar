#!/usr/bin/env python3
"""
A small web service for printing similar words in the English language.
"""
import json
import sys
import time
import argparse
import logging

from collections import defaultdict
from flask import Flask, request, g
from dataclasses import dataclass
from dataclasses_json import dataclass_json

__author__ = "Roy Moore"
__license__ = "MIT"
__version__ = "1.0.0"

# noinspection SpellCheckingInspection
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%H:%M:%S',
                    handlers=[logging.StreamHandler(sys.stdout)])


class FancyDictionary:
    def __init__(self, path, logger):
        """
        :param str path: path of source dictionary
        """
        self.logger = logger
        self._data, self.total_words = self._load_data_file(path)

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
        Load a dictionary txt file
        :param str path: path of data source
        """
        start_time = time.time()
        data = defaultdict(list)
        total_words = 0

        with open(path, "r") as fileHandler:
            for line in fileHandler:
                total_words += 1
                word = line.strip()  # Need to stripe as each line (except last one) will contain new line character
                sorted_word = self._sort_word(word)  # get the sorted version of the word
                data[sorted_word] += [word]  # Insert the data to the DB

        end_time = time.time()

        self.logger.info("DB loaded successfully (loaded in %.5fs)", end_time - start_time)
        self.logger.debug(f"Words count = {total_words}, "
                          f"DB Keys = {len(data.keys())}, "
                          f"DB Values = {sum([len(data[x]) for x in data if isinstance(data[x], list)])}")

        return data, total_words


class StreamingMovingAverage:
    def __init__(self, window_size):
        self.window_size = window_size
        self.values = []
        self.sum = 0

    def process(self, value):
        print(value)
        self.values.append(value)
        self.sum += value
        if len(self.values) > self.window_size:
            self.sum -= self.values.pop(0)
        print(float(self.sum), len(self.values))
        return int(float(self.sum) / len(self.values))


class Server:
    @dataclass_json
    @dataclass
    class StatInfo:
        totalWords: int
        totalRequests: int = 0
        avgProcessingTimeNs: int = 0

    def __init__(self, debug, host, port, logger):
        self.debug = debug
        self.host = host
        self.port = port
        self.logger = logger
        self.db = FancyDictionary(args.file, logger)
        self.stat_info = self.StatInfo(totalWords=self.db.total_words)
        self.avg_time_calc = StreamingMovingAverage(window_size=10)

    BASE_URL = "/api/"
    VERSION_URL = BASE_URL + 'v1/'
    PING_URL = VERSION_URL + 'ping'
    SIMILAR_URL = VERSION_URL + 'similar'
    STATS_URL = VERSION_URL + 'stats'

    def run(self):
        app = Flask(__name__)

        @app.before_request
        def before_request():
            g.request_start_time = time.time()
            g.request_time = lambda: "%.f" % ((time.time() - g.request_start_time) * 100000000)  # Convert to nano

        @app.route(self.PING_URL, methods=['GET'])
        def get_test():
            """
            Test the server
            """
            return "pong"

        @app.route(self.SIMILAR_URL, methods=['GET'])
        def get_similar():
            """
            Returns all words in the dictionary that has the same permutation as the word
            :rtype: str
            """
            self.StatInfo.totalRequests += 1
            requested_word = request.args.get('word')
            result_dict = dict()
            result_dict['similar'] = self.db.check(requested_word)  # TODO: change to result object?
            result_json = json.dumps(result_dict)
            request_time = int(g.request_time())
            log.debug(f"request time {request_time}ns")
            self.stat_info.avgProcessingTimeNs = self.avg_time_calc.process(request_time)

            return result_json

        @app.route(self.STATS_URL, methods=['GET'])
        def get_stats():
            """
            Return general statistics
            :rtype: str
            """
            return self.stat_info.to_json()

        app.run(debug=self.debug, host=self.host, port=self.port)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Print Similar Web Service')
    parser.add_argument("-d", "--debug", action="store_true", default=False, help="enable debug mode")
    parser.add_argument("-n", "--host", action="store", type=str, default="0.0.0.0", help="hostname to listen on")
    parser.add_argument("-p", "--port", action="store", type=int, default=8000, help="port of the webserver")
    parser.add_argument("-f", "--file", action="store", type=str, default="words_clean.txt", help="source data file")
    args = parser.parse_args()

    log = logging.getLogger(__name__)

    server = Server(debug=args.debug, host=args.host, port=args.port, logger=log)
    server.run()
