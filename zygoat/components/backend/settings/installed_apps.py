import logging

from zygoat.components import SettingsComponent

log = logging.getLogger()


class InstalledApps(SettingsComponent):
    def create(self):
        exported_values = ["ALLOWED_HOSTS", "DATABASES"]

        red = self.parse()
        apps_list = red.find("name", value="INSTALLED_APPS").parent.value

        log.info("Adding DRF to installed apps")
        apps_list.append("'rest_framework'")

        log.info("Adding backend app to installed apps")
        apps_list.append("'zygoat_django'")

        log.info("Removing default components exported by zygoat_django")

        for value in exported_values:
            index = red.find("name", value=value).parent.index_on_parent

            # Delete the blank line following it as well
            del red[index]
            del red[index]

        log.info("Dumping installed apps node")
        self.dump(red)

    @property
    def installed(self):
        red = self.parse()
        return (
            "zygoat_django"
            in red.find("name", value="INSTALLED_APPS").parent.value.to_python()
        )


installed_apps = InstalledApps()
