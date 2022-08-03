FROM python:latest

RUN pip install --upgrade pip poetry

RUN mkdir /code
WORKDIR /code

COPY poetry.lock pyproject.toml /code/
RUN poetry install --no-dev

COPY . .

CMD poetry run ./manage.py wait_for_db && poetry run ./manage.py migrate && poetry run ./manage.py createcachetable && poetry run gunicorn backend.wsgi
