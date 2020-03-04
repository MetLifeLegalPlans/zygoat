import logging

from zygoat.components import SettingsComponent

log = logging.getLogger()


secure_cookie_string = """\
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
"""


class Cookies(SettingsComponent):
    def create(self):
        red = self.parse()

        log.info("Adding cookie configuration")

        red.extend(
            [
                "\n",
                "\n",
                "# Cookies",
                "\n",
                "SHARED_DOMAIN = env.str('DJANGO_SHARED_DOMAIN', default=None)",
                "\n",
                "CSRF_COOKIE_DOMAIN = SHARED_DOMAIN",
                "\n",
                "SESSION_COOKIE_DOMAIN = SHARED_DOMAIN",
                "\n",
                "SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'",
                "\n",
                "SESSION_COOKIE_AGE = 604800  # One week in seconds",
                "\n",
                secure_cookie_string,
            ]
        )

        self.dump(red)

    @property
    def installed(self):
        red = self.parse()
        return red.find("name", value="SESSION_ENGINE") is not None


cookies = Cookies()
