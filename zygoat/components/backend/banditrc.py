from zygoat.components import FileComponent
from zygoat.components.backend import resources


class BanditRC(FileComponent):
    base_path = "backend/tests"
    filename = ".banditrc"
    resource_pkg = resources


banditrc = BanditRC()
