import logging
import time

from dataclasses import dataclass
from dataclasses_json import dataclass_json
from quart import Quart, request, g, jsonify

from src.data import FancyDictionary
from src.utils import StreamingMovingAverage

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
        self.avg_time_calc = StreamingMovingAverage(window_size=self.SAMPLE_WINDOW_SIZE)

    def run(self):
        app = Quart(__name__)

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
            self.stat_info.totalRequests += 1
            requested_word = request.args.get('word')
            result_dict = dict()
            result_dict['similar'] = await self.db.check(requested_word)  # Note: changing to object degrades performance x6
            request_time = int(g.request_time())
            logging.debug(f"request time {request_time}ns")
            self.stat_info.avgProcessingTimeNs = await self.avg_time_calc.update(request_time)

            return jsonify(result_dict)

        @app.route(STATS_URL, methods=['GET'])
        async def get_stats():
            """
            Return general statistics
            :rtype: str
            """
            self.stat_info.avgProcessingTimeNs = self.avg_time_calc.calculate()

            return self.stat_info.to_json()

        app.run(debug=self.debug, host=self.host, port=self.port)
