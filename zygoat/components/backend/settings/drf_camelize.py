import logging

from zygoat.components import SettingsComponent

log = logging.getLogger()

# If this string starts with a blank line, RedBaron completely ignores it
settings_string = """REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": (
        "djangorestframework_camel_case.render.CamelCaseJSONRenderer",
        "djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer",
    ),
    "DEFAULT_PARSER_CLASSES": (
        "djangorestframework_camel_case.parser.CamelCaseFormParser",
        "djangorestframework_camel_case.parser.CamelCaseMultiPartParser",
        "djangorestframework_camel_case.parser.CamelCaseJSONParser",
    ),
}"""


class DRF_Camelize(SettingsComponent):
    def create(self):
        red = self.parse()

        red.extend(["\n", settings_string])

        log.info("Dumping DRF camelize configuration")
        self.dump(red)

    @property
    def installed(self):
        red = self.parse()
        node = red.find("name", value="REST_FRAMEWORK")

        if node is None:
            return False

        return "Camel" in red.find("name", value="REST_FRAMEWORK").parent.value.dumps()


drf_camelize = DRF_Camelize()
