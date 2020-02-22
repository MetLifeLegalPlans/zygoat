import os
import logging

log = logging.getLogger()


def walk_up():
    path = os.getcwd()

    while True:
        yield path

        if path == '/':
            raise StopIteration

        path = os.path.join(path, '..')


def find_nearest(file_name):
    try:
        for path in walk_up():
            target = os.path.join(path, file_name)

            # If the file is not found, walk_up() will error out
            if os.path.isfile(target):
                log.debug(f'Found {target}')
                return target
    except StopIteration as e:
        log.critical(f'Unable to locate file_name in current or any parent directory, exiting')
        raise e
