#!/usr/bin/env python3
"""
Runnable server for Print Similar web service
"""
import argparse

from code.app import Server
from utils import config_logs

__author__ = "Roy Moore"
__license__ = "MIT"
__version__ = "1.0.0"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Print Similar Web Service')
    parser.add_argument("-d", "--debug", action="store_true", default=False, help="enable debug mode")
    parser.add_argument("-n", "--host", action="store", type=str, default="0.0.0.0", help="hostname to listen on")
    parser.add_argument("-p", "--port", action="store", type=int, default=8000, help="port of the webserver")
    parser.add_argument("-f", "--datafile", action="store", type=str, default="../words_clean.txt",
                        help="source data file")
    args = parser.parse_args()

    logger = config_logs(__name__)

    server = Server(datafile=args.datafile)
    server.get_app().run(host=args.host, port=args.port, debug=args.debug)
