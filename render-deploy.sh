set -e

poetry lock
poetry run flask --app src.app db upgrade
poetry run gunicorn src.wsgi:app