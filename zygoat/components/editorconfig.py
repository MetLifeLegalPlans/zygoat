from zygoat.components import FileComponent, resources


class EditorConfig(FileComponent):
    filename = '.editorconfig'
    resource_pkg = resources


editorconfig = EditorConfig()
