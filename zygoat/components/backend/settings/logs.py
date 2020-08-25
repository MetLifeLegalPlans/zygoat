import logging

from zygoat.components import SettingsComponent

log = logging.getLogger()


settings_string = """LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"stderr": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["stderr"], "level": "INFO"},
}"""


class Logs(SettingsComponent):
    def create(self):
        red = self.parse()

        log.info("Adding logging configuration")

        red.extend(
            ["\n", settings_string, "\n",]
        )

        self.dump(red)

    @property
    def installed(self):
        red = self.parse()
        return red.find("name", value="LOGGING") is not None


logs = Logs()
