from zygoat.components import FileComponent, resources


class PreCommitConfig(FileComponent):
    filename = '.pre-commit-config.yaml'
    resource_pkg = resources


precommitconfig = PreCommitConfig()
