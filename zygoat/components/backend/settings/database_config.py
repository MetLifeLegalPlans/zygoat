import logging

from zygoat.components import SettingsComponent

log = logging.getLogger()


class DatabaseConfig(SettingsComponent):
    def create(self):
        red = self.parse()
        db_node = red.find("name", value="DATABASES").parent

        log.info("Inserting DB URL configuration")
        red.insert(
            red.index(db_node),
            "db_config = env.db_url('DATABASE_URL', default='postgres://postgres:postgres@db/postgres')",
        )

        log.info("Settings database config")
        db_node.value = "{'default': db_config}"

        log.info("Dumping database connection node")
        self.dump(red)

    @property
    def installed(self):
        red = self.parse()
        return "db_config" in red.find("name", value="DATABASES").parent.value.dumps()


database_config = DatabaseConfig()
