from zygoat.components.codebuild import CodeBuild

from . import resources


class CodeBuildCypress(CodeBuild):
    filename = "e2e.yml"
    resource_pkg = resources


codebuild = CodeBuildCypress()
