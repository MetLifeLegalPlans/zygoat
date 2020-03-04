from zygoat.components import FileComponent


class PreCommitConfig(FileComponent):
    filename = ".pre-commit-config.yaml"


precommitconfig = PreCommitConfig()
