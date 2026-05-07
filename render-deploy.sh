#!/usr/bin/env bash
set -e

poetry run flask --app src.app db upgrade
poetry run gunicorn src.wsgi:app --bind 0.0.0.0:$PORT