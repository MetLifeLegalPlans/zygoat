import base64
import logging
import os

from zygoat.components import SettingsComponent

log = logging.getLogger()


class SecretKey(SettingsComponent):
    def create(self):
        red = self.parse()
        key_node = red.find("name", value="SECRET_KEY").parent

        log.info("Generating default secret key")
        default_key = base64.b64encode(os.urandom(32)).decode("utf-8")

        log.info("Relocating default secret key")
        key_node.value = f"prod_required_env('DJANGO_SECRET_KEY', default='{default_key}')"

        log.info("Dumping secret key node")
        self.dump(red)

    def update(self):
        red = self.parse()

        log.info("Copying secret key value from previous settings")
        key_node = red.find("name", value="SECRET_KEY").parent
        key_node.value = self.parent.existing_secret_key

        self.dump(red)

    @property
    def installed(self):
        return bool(getattr(self.parent, "existing_secret_key", None))


secret_key = SecretKey()
