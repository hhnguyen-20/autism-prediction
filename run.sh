#!/bin/sh
set -e
gunicorn api.wsgi --log-file -