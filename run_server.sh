#!/usr/bin/env bash

export PYTHONPATH="${PYTHONPATH}:./code"

hypercorn server:app -b 0.0.0.0:8000