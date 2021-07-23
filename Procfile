web: gunicorn CHATRU.wsgi --log-file -
web22: daphne chat.asgi:channel_layer --port $PORT --bind 0.0.0.0 -v2
web2: daphne CHATRU.routing:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker channel_layer -v2
