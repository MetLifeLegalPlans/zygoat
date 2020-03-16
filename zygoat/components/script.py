from zygoat.components import FileComponent


class Script(FileComponent):
    base_path = "scripts"


class CiStart(Script):
    filename = "ci-start.sh"
    executable = True


cistart = CiStart()
