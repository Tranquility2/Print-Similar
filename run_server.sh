#!/usr/bin/env bash

export PYTHONPATH="${PYTHONPATH}:./src"

hypercorn server:app -b 0.0.0.0:8000