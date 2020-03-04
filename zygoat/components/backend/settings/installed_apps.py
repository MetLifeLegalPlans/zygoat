import logging

from zygoat.components import SettingsComponent

log = logging.getLogger()


class InstalledApps(SettingsComponent):
    def create(self):
        red = self.parse()
        apps_list = red.find("name", value="INSTALLED_APPS").parent.value

        log.info("Adding backend app to installed apps")
        apps_list.append("'backend'")

        log.info("Dumping installed apps node")
        self.dump(red)

    @property
    def installed(self):
        red = self.parse()
        return "backend" in red.find("name", value="INSTALLED_APPS").parent.value.to_python()


installed_apps = InstalledApps()
