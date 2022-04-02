#!/bin/sh

set -e

python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py migrate

uwsgi --socket :9000 --workers 4 --master --enable-threads --module app.wsgi
# port 9000 is the port for communication with nginx
# 4 workers is default for most cases
# "--master" ensures the app works in foreground

