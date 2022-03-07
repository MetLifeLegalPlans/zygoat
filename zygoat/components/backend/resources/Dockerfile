FROM python:latest

RUN pip install --upgrade pip poetry

RUN mkdir /code
WORKDIR /code

COPY poetry.lock pyproject.toml /code/
RUN poetry install

COPY . .

CMD poetry run ./manage.py wait_for_db && poetry run ./manage.py migrate && poetry run ./manage.py createcachetable && poetry run gunicorn -w 4 -b 0.0.0.0:3000 backend.asgi -k zygoat_django.uvicorn_worker.ZygoatUvicornWorker
