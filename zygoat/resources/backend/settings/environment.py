import environ
import os
import sys

from typing import Any

env = environ.Env()

PRODUCTION = env.bool("DJANGO_PRODUCTION", default=False)
"""
Whether or not the app is running in production.

If `True`, `Debug` is explicitly set to `False` to avoid leaking information
"""

DEBUG = False if PRODUCTION else env.bool("DJANGO_DEBUG", default=True)
"""
Used internally by Django to decide how much debugging context is sent to the
browser when a failure occurs.

Cannot be `True` if `PRODUCTION` is `True`
"""

TESTING = "pytest" in sys.modules
"""
Whether or not we're running as part of a test suite.
"""


def prod_required_env(key: str, default: Any, method: str = "str") -> Any:
    """
    Throw an exception if PRODUCTION is true and the environment key is not provided
    See also:
       - [django-environ](https://github.com/joke2k/django-environ)
       - [django-environ supported types](https://github.com/joke2k/django-environ#supported-types)
    """
    if PRODUCTION:
        default = environ.Env.NOTSET
    return getattr(env, method)(key, default)


ALLOWED_HOSTS = [prod_required_env("DJANGO_ALLOWED_HOST", default="*")]
"""
Sets the list of valid ``HOST`` header values. Typically this is handled by
a reverse proxy in front of the deploy Django application. In development,
this is provided by the Caddy reverse proxy.
"""

db_config = env.db_url("DATABASE_URL", default="postgres://postgres:postgres@db/postgres")
"""
Parses the `DATABASE_URL` environment variable into a django `databases` dictionary.

Uses a standard database URI schema.
"""

DATABASES = {"default": db_config}
"""
[Django databases configuration value](https://docs.djangoproject.com/en/3.1/ref/settings/#databases).

The default entry is generated automatically from `db_config`. If you need more than one database or a
different default setup, you can modify this value in your application's `settings.py` file.
"""

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
