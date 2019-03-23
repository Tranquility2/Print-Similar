#!/usr/bin/env python3

__author__ = "Roy Moore"
__license__ = "MIT"
__version__ = "1.0.0"

from flask import Flask

APP_PORT = 8000
APP_DEBUG = True

app = Flask(__name__)


@app.route('/')
def index():
    return "Test"


if __name__ == '__main__':
    app.run(debug=APP_DEBUG, host='0.0.0.0', port=APP_PORT)
