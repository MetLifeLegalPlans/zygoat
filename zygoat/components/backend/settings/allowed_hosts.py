import logging

from zygoat.components import SettingsComponent

log = logging.getLogger()


class AllowedHosts(SettingsComponent):
    def create(self):
        red = self.parse()
        host_list = red.find("name", value="ALLOWED_HOSTS").parent.value

        log.info("Adding allowed host environment config")
        host_list.append("env('DJANGO_ALLOWED_HOST', default='*')")

        log.info("Dumping installed apps node")
        self.dump(red)

    @property
    def installed(self):
        red = self.parse()
        return (
            "DJANGO_ALLOWED_HOST"
            in red.find("name", value="ALLOWED_HOSTS").parent.value.dumps()
        )


allowed_hosts = AllowedHosts()
