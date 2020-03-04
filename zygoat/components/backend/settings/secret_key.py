import logging

from zygoat.components import SettingsComponent

log = logging.getLogger()


class SecretKey(SettingsComponent):
    def create(self):
        red = self.parse()
        key_node = red.find("name", value="SECRET_KEY").parent

        log.info("Retrieving default secret key")
        default_key = key_node.value.to_python()

        log.info("Relocating default secret key")
        key_node.value = f"env.str('DJANGO_SECRET_KEY', default='{default_key}')"

        log.info("Dumping secret key node")
        self.dump(red)

    @property
    def installed(self):
        red = self.parse()
        return "env.str(" in red.find("name", value="SECRET_KEY").parent.value.dumps()


secret_key = SecretKey()
