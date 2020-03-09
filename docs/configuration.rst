Configuration
=============

zygoat_settings.yml
-------------------

Upon project creation, ``zygoat`` will create a ``zygoat_settings.yml`` file. Currently, this file only contains the name of the project being created and a list of components to exclude.

Example file::

  name: goat-hugging-instructions
  exclude:
    - DockerCompose
    - Backend__DockerFile
    - Frontend__DockerFile
