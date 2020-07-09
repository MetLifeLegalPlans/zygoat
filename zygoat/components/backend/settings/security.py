import logging

from zygoat.components import SettingsComponent

log = logging.getLogger()

security_headers = """\
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
"""


class Security(SettingsComponent):
    def create(self):
        red = self.parse()

        log.info("Adding security headers")

        red.extend(
            [
                "\n",
                "# Set security headers",
                "\n",
                "X_FRAME_OPTIONS = 'DENY'",
                "\n",
                security_headers,
            ]
        )
        self.dump(red)

    @property
    def installed(self):
        red = self.parse()
        return red.find("name", value="SECURE_HSTS_SECONDS") is not None


security = Security()
