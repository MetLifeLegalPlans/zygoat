CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": prod_required_env("DJANGO_REDIS_CACHE_URL", "redis://cache:6379/0"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}
"""
Configures the default cache to point to the zygoat generated docker container.
"""

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
