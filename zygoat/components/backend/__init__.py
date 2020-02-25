import logging

from .. import Component
from zygoat.utils.files import use_dir
from zygoat.utils.shell import run

import virtualenv

log = logging.getLogger()


class Backend(Component):
    def create(self):
        log.info('Installing django at a user level to generate the project')
        run(['pip', 'install', '--user', '--upgrade', 'django'])

        log.info('Creating the django project')
        run(['django-admin', 'startproject', 'backend'])

        with use_dir('backend'):
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


backend = Backend()


__all__ = [backend]
