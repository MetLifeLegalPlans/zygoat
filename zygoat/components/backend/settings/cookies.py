import logging

from zygoat.components import SettingsComponent

log = logging.getLogger()


class Cookies(SettingsComponent):
    def create(self):
        red = self.parse()

        log.info("Adding cookie configuration")

        red.extend(
            [
                "\n",
                "\n",
                "# Cookies",
                "SHARED_DOMAIN = prod_required_env('DJANGO_SHARED_DOMAIN', default=None)",
                "CSRF_COOKIE_DOMAIN = SHARED_DOMAIN",
                "CSRF_TRUSTED_ORIGINS = SHARED_DOMAIN and [f'.{SHARED_DOMAIN}']",
                "SESSION_COOKIE_DOMAIN = SHARED_DOMAIN",
                "SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'",
                "SESSION_COOKIE_AGE = 3600  # One hour in seconds",
                "SESSION_COOKIE_SECURE = True",
                "CSRF_COOKIE_SECURE = True",
                "\n",
            ]
        )

        self.dump(red)

    @property
    def installed(self):
        red = self.parse()
        return red.find("name", value="SESSION_ENGINE") is not None


cookies = Cookies()
