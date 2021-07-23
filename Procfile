web: gunicorn CHATRU.wsgi --log-file -
web2: daphne CHATRU.routing:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker channel_layer -v2
