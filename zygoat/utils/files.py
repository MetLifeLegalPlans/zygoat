import os
import logging

from click import style

log = logging.getLogger()


def walk_up():
    """
    Generator expression to provide paths up to the system root

    Does not work on Windows, but then again, neither does Zygoat
    """
    path = os.getcwd()

    while True:
        log.debug(f'Searching {style(path, bold=True)}')
        yield path

        if path == '/':
            raise FileNotFoundError

        path = os.path.dirname(path)


def find_nearest(file_name):
    """
    Returns the absolute path to the nearest existing file matching file_name

    :param file_name: Name of the file to locate
    """
    try:
        for path in walk_up():
            target = os.path.join(path, file_name)

            # If the file is not found, walk_up() will error out
            if os.path.exists(target):
                log.debug(f'Found {file_name} in {os.path.dirname(target)}')
                return target
    except FileNotFoundError:
        raise FileNotFoundError(f'Unable to locate {file_name} in current or any parent directory')
