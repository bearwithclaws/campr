#!/bin/bash
cd /srv/campr
source $HOME/.virtualenvs/campr/bin/activate
python frontend/manage.py collectstatic --noinput
python server.py --port 8000
