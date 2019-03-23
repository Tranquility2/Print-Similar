#!/usr/bin/env python3
"""
A small web service for printing similar words in the English language.
"""
__author__ = "Roy Moore"
__license__ = "MIT"
__version__ = "1.0.0"

import argparse

from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return "Test"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Print Similar Web Service')
    parser.add_argument("-d", "--debug", action="store_true", default=False, help="enable debug mode")
    parser.add_argument("-n", "--host", action="store", type=str, default="0.0.0.0", help="hostname to listen on")
    parser.add_argument("-p", "--port", action="store", type=int, default=8000, help="port of the webserver")
    args = parser.parse_args()
    app.run(debug=args.debug, host=args.host, port=args.port)
