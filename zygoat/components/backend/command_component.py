import os

from zygoat.constants import Projects
from zygoat.components import Component, FileComponent
from zygoat.components.backend import resources


class ManagementCommand(Component):
    pass


class CommandComponent(FileComponent):
    resource_pkg = resources
    base_path = os.path.join(Projects.BACKEND, "backend", "management", "commands")


class ManagementInit(FileComponent):
    base_path = os.path.join(Projects.BACKEND, "backend", "management")
    filename = "__init__.py"


class CommandInit(FileComponent):
    base_path = os.path.join(Projects.BACKEND, "backend", "management", "commands")
    filename = "__init__.py"


class WaitCommand(CommandComponent):
    filename = "wait_for_db.py"


class StaffCommand(CommandComponent):
    filename = "set_staff.py"


management_command = ManagementCommand(
    sub_components=[ManagementInit(), CommandInit(), WaitCommand(), StaffCommand()]
)
