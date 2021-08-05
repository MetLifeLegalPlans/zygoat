FROM python:latest

RUN mkdir /code
WORKDIR /code

COPY . .
RUN pip install -r requirements.txt

CMD ./manage.py wait_for_db && ./manage.py migrate && ./manage.py createcachetable && gunicorn -w 4 -b 0.0.0.0:3000 backend.asgi -k zygoat_django.uvicorn_worker.ZygoatUvicornWorker
