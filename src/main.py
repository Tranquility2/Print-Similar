#!/usr/bin/env python3
"""
A small web service for printing similar words in the English language.
"""
import argparse
import logging

from src.app import Server

__author__ = "Roy Moore"
__license__ = "MIT"
__version__ = "1.0.0"

# noinspection SpellCheckingInspection
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%H:%M:%S')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Print Similar Web Service')
    parser.add_argument("-d", "--debug", action="store_true", default=False, help="enable debug mode")
    parser.add_argument("-n", "--host", action="store", type=str, default="0.0.0.0", help="hostname to listen on")
    parser.add_argument("-p", "--port", action="store", type=int, default=8000, help="port of the webserver")
    parser.add_argument("-f", "--file", action="store", type=str, default="words_clean.txt", help="source data file")
    args = parser.parse_args()

    log = logging.getLogger(__name__)

    server = Server(file=args.file, debug=args.debug, host=args.host, port=args.port, logger=log)
    server.run()
