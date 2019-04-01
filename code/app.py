"""
Print Similar - Web service for printing similar words in the English language.
"""
import time
import pymongo

from dataclasses import dataclass
from dataclasses_json import dataclass_json
from quart import Quart, request, g, jsonify

from code.data import FancyDictionary
from utils import config_logs

ROOT_URL = "/"
BASE_URL = ROOT_URL + "api/"
VERSION_URL = BASE_URL + 'v1/'
PING_URL = VERSION_URL + 'ping'
SIMILAR_URL = VERSION_URL + 'similar'
STATS_URL = VERSION_URL + 'stats'


def get_mongo_collection():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["local"]
    collection = db["requests"]

    return collection


@dataclass_json
@dataclass
class StatInfo:
    totalWords: int
    totalRequests: int = 0
    avgProcessingTimeNs: int = 0


class Server:
    def __init__(self, datafile):
        self.collection = get_mongo_collection()
        self.logger = config_logs(__name__)
        self.db = FancyDictionary(datafile, self.logger)
        self.stat_info = StatInfo(totalWords=self.db.total_words)

    def get_app(self):
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
            result_dict = dict()
            requested_word = request.args.get('word')
            # Note: changing to check object degrades performance x6
            result_dict['similar'] = await self.db.check(requested_word)
            request_time = int(g.request_time())
            self.logger.debug(f"request time {request_time}ns")
            # Update collection regarding request time
            request_info_string = {"handling_time": request_time}
            self.collection.insert_one(request_info_string)

            return jsonify(result_dict)

        @app.route(STATS_URL, methods=['GET'])
        async def get_stats():
            """
            Return general statistics
            :rtype: str
            """
            # if len(app.values):
            #     self.stat_info.avgProcessingTimeNs = int(float(app.sum) / len(app.values))  # calculate average

            self.stat_info.totalRequests = self.collection.count()
            if self.stat_info.totalRequests:
                pipeline = [{"$group": {"_id": None, "avg": {"$avg": "$handling_time"}}}]
                self.stat_info.avgProcessingTimeNs = int(self.collection.aggregate(pipeline).next()['avg'])

            return self.stat_info.to_json()

        return app
