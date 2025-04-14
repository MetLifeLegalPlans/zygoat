# Redis
CACHE_URL = prod_required_env("DJANGO_REDIS_CACHE_URL", default="redis://cache:6379/1")
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": CACHE_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SOCKET_TIMEOUT": env.int("DJANGO_REDIS_TIMEOUT", default=5),
            "SOCKET_CONNECT_TIMEOUT": env.int("DJANGO_REDIS_CONNECTION_TIMEOUT", default=5),
        },
    }
}
"""
Configures the default cache to point to the zygoat generated docker container.
"""

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
