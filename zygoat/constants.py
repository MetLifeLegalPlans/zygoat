import os

from importlib_metadata import version

from box import Box


config_file_name = "zygoat_settings.yml"

phase_function_names = [
    "create",
    "update",
    "delete",
    "list",
]
project_dir_names = [
    "backend",
    "frontend",
    "cache",
]

Phases = Box([(t.upper(), t) for t in phase_function_names])
Projects = Box([(t.upper(), t) for t in project_dir_names])
Images = Box({"NODE": "NODE", "PYTHON": "PYTHON"})

ConfigDefaults = Box({"images": {"NODE": "node:latest", "PYTHON": "python:latest"}})

FrontendUtils = os.path.join(Projects.FRONTEND, "zg_utils")

__version__ = version("zygoat")
