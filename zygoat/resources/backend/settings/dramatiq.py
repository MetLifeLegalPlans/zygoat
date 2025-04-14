# Dramatiq
CORE_DRAMATIQ_MIDDLEWARE = [
    "dramatiq.middleware.AgeLimit",
    "dramatiq.middleware.TimeLimit",
    "dramatiq.middleware.Callbacks",
    "dramatiq.middleware.Retries",
    "django_dramatiq.middleware.DbConnectionsMiddleware",
    "django_dramatiq.middleware.AdminMiddleware",
    "dramatiq.middleware.Pipelines",
]


DRAMATIQ_BROKER = {
    "BROKER": "dramatiq.brokers.redis.RedisBroker",
    "OPTIONS": {
        "url": CACHE_URL,
    },
    "MIDDLEWARE": [
        "dramatiq.middleware.Prometheus",
    ]
    + CORE_DRAMATIQ_MIDDLEWARE,
}

DRAMATIQ_RESULT_BACKEND = {
    "BACKEND": "dramatiq.results.backends.redis.RedisBackend",
    "BACKEND_OPTIONS": {
        "url": CACHE_URL,
    },
    "MIDDLEWARE_OPTIONS": {"result_ttl": 1000 * 60 * 10},
}

if TESTING:
    DRAMATIQ_RESULT_BACKEND = {
        "BACKEND": "dramatiq.results.backends.StubBackend",
        "MIDDLEWARE_OPTIONS": {"result_ttl": 1000 * 60 * 10},
    }

    DRAMATIQ_BROKER = {
        "BROKER": "dramatiq.brokers.stub.StubBroker",
        "OPTIONS": {},
        "MIDDLEWARE": CORE_DRAMATIQ_MIDDLEWARE,
    }
