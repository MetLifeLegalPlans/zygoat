import logging

from zygoat.components import SettingsComponent

log = logging.getLogger()

# If this string starts with a blank line, RedBaron completely ignores it
settings_string = """def prod_required_env(key, default, method="str"):
    \"\"\"Throw an exception if PRODUCTION is true and key is not provided\"\"\"
    if PRODUCTION:
        default = environ.Env.NOTSET
    return getattr(env, method)(key, default)

"""


class Env(SettingsComponent):
    def create(self):
        red = self.parse()

        first_import_index = red.index(red.find("importnode"))

        log.info("Inserting environ import into django settings")
        red.insert(first_import_index + 1, "import environ")

        log.info("Inserting environ constructor")

        red.insert(first_import_index + 2, "env = environ.Env()")

        log.info("Inserting prod_required_env function")
        index = red.index(red.find("name", "PRODUCTION").parent)
        red.insert(index + 1, "\n")
        red.insert(index + 2, "\n")
        red.insert(index + 3, settings_string)

        self.dump(red)

    @property
    def installed(self):
        red = self.parse()
        return red.find("def", "prod_required_env") is not None


env = Env()
