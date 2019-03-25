import logging
import time

from dataclasses import dataclass
from dataclasses_json import dataclass_json
from quart import Quart, request, g, jsonify

from src.data import FancyDictionary

logging.getLogger()

ROOT_URL = "/"
BASE_URL = ROOT_URL + "api/"
VERSION_URL = BASE_URL + 'v1/'
PING_URL = VERSION_URL + 'ping'
SIMILAR_URL = VERSION_URL + 'similar'
STATS_URL = VERSION_URL + 'stats'


@dataclass_json
@dataclass
class StatInfo:
    totalWords: int
    totalRequests: int = 0
    avgProcessingTimeNs: int = 0


class Server:
    SAMPLE_WINDOW_SIZE = 10

    def __init__(self, file, debug, host, port, logger):
        self.debug = debug
        self.host = host
        self.port = port
        self.logger = logger
        self.db = FancyDictionary(file, logger)
        self.stat_info = StatInfo(totalWords=self.db.total_words)

    def run(self):
        app = Quart(__name__)
        # Moving average parameters
        app.window_size = self.SAMPLE_WINDOW_SIZE
        app.values = []
        app.sum = 0

        @app.before_request
        async def before_request():
            """
            Used to setup time calculation
            """
            g.request_start_time = time.time()
            g.request_time = lambda: "%.f" % ((time.time() - g.request_start_time) * 100000000)  # Convert to nano

        @app.route(PING_URL, methods=['GET'])
        async def get_test():
            """
            Test the server
            """
            return "pong"

        @app.route(SIMILAR_URL, methods=['GET'])
        async def get_similar():
            """
            Returns all words in the dictionary that has the same permutation as the word
            :rtype: str
            """
            async def update(value):
                """
                Store a given value for calculation
                :param int value:
                """
                app.values.append(value)
                app.sum += value
                if len(app.values) > app.window_size:
                    app.sum -= app.values.pop(0)

            result_dict = dict()
            self.stat_info.totalRequests += 1
            requested_word = request.args.get('word')
            # Note: changing to check object degrades performance x6
            result_dict['similar'] = await self.db.check(requested_word)
            request_time = int(g.request_time())
            logging.debug(f"request time {request_time}ns")
            self.stat_info.avgProcessingTimeNs = await update(request_time)

            return jsonify(result_dict)

        @app.route(STATS_URL, methods=['GET'])
        async def get_stats():
            """
            Return general statistics
            :rtype: str
            """
            self.stat_info.avgProcessingTimeNs = int(float(app.sum) / len(app.values))  # calculate average

            return self.stat_info.to_json()

        app.run(debug=self.debug, host=self.host, port=self.port)
