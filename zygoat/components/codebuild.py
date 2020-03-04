from zygoat.components import FileComponent


class CodeBuild(FileComponent):
    base_path = "codebuild"


class CodeBuildDefault(CodeBuild):
    filename = "codebuild.yml"


codebuild = CodeBuildDefault()
