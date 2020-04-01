from zygoat.components import FileComponent, Component


class CodeBuild(Component):
    pass


class CodeBuildFile(FileComponent):
    base_path = "codebuild"
    overwrite = False


class Security(CodeBuildFile):
    filename = "security.yml"


class Linting(CodeBuildFile):
    filename = "linting.yml"


class Testing(CodeBuildFile):
    filename = "testing.yml"


codebuild = CodeBuild(sub_components=[Security(), Linting(), Testing()])
