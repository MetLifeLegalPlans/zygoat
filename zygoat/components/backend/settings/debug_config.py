import logging

from zygoat.components import SettingsComponent

log = logging.getLogger()
log.setLevel(logging.INFO)


class DebugConfig(SettingsComponent):
    def create(self):
        red = self.parse()
        secret_key_index = red.index(red.find("name", value="SECRET_KEY").parent)

        log.info("Inserting PRODUCTION environment variable")
        red.insert(
            secret_key_index - 2, "PRODUCTION = env.bool('DJANGO_PRODUCTION', default=False)"
        )

        debug_node = red.find("name", value="DEBUG").parent

        log.info("Disabling debug in production")
        debug_node.value = "False if PRODUCTION else env.bool('DJANGO_DEBUG', default=True)"

        log.info("Dumping debug configuration node")
        self.dump(red)

    @property
    def installed(self):
        red = self.parse()
        return "PRODUCTION" in red.find("name", value="DEBUG").parent.dumps()


debug_config = DebugConfig()
