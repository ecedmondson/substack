#!/bin/bash

MAX_RETRIES=5
RETRIES=0
until poetry run python manage.py migrate; do
   RETRIES=`expr $RETRIES + 1`
   if [[ "$RETRIES" -eq "$MAX_RETRIES" ]]; then
       echo "Retry Limit Exceeded. Aborting..."
       exit 1
   fi
   sleep 2
done

poetry run python manage.py collectstatic
poetry run python manage.py runserver 0.0.0.0:8000
