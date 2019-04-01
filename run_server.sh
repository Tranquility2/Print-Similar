#!/usr/bin/env bash

export PYTHONPATH="${PYTHONPATH}:./code"

# Prep Mongo
service mongodb start
mongo local --eval 'db.createCollection("requests");'

hypercorn --workers 4 server:app -b 0.0.0.0:80
