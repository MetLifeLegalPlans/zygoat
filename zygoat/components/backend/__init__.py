import logging
import os

from .. import Component
from zygoat.utils.files import use_dir
from zygoat.utils.shell import run
from zygoat.constants import Projects

from .dockerfile import dockerfile

import virtualenv

log = logging.getLogger()


class Backend(Component):
    def create(self):
        log.info('Installing django at a user level to generate the project')
        run(['pip', 'install', '--user', '--upgrade', 'django'])

        log.info('Creating the django project')
        run(['django-admin', 'startproject', Projects.BACKEND])

        with use_dir(Projects.BACKEND):
            log.info('Creating and activating a virtualenv for the project')
            virtualenv.cli_run(['venv'])

            # Programmatically activate the virtualenv in the current session
            venv_file = 'venv/bin/activate_this.py'
            exec(open(venv_file).read(), {'__file__': venv_file})

            log.info('Installing project dependencies and creating a requirements file')
            run([
                'pip',
                'install',
                '--upgrade',
                'django',
                'psycopg2-binary',
                'django-cors-headers',
                'djangorestframework',
                'django-environ',
            ])

            freeze_result = run([
                'pip',
                'freeze',
            ], capture_output=True)

            with open('requirements.txt', 'w') as f:
                f.write(freeze_result.stdout.decode())

    def update(self):
        pass

    def delete(self):
        pass

    def deploy(self):
        pass

    @property
    def installed(self):
        return os.path.exists(Projects.BACKEND)


backend = Backend(sub_components=[dockerfile])
