import os
from shutil import which

from .shell import run
from .files import use_dir, repository_root
from zygoat.constants import Projects

pip = which("pip")
dev_file_name = "requirements.dev.txt"
prod_file_name = "requirements.txt"


def freeze():
    return run([pip, "freeze"], capture_output=True).stdout.decode().split("\n")


def packages_to_map(arr):
    result = {}

    for package_line in arr:
        # Ignore `-r requirements.txt` and other non-package related lines
        if "=" not in package_line:
            if "git://" in package_line:
                result[package_line] = package_line
            continue
        package = package_line.split("=")[0]
        result[package] = package_line

    return result


def dump_dependencies(package_map, dev=False):
    file_name = dev_file_name if dev else prod_file_name

    with repository_root():
        with use_dir(Projects.BACKEND):
            with open(file_name, "w") as f:
                if dev:
                    f.write(f"-r {prod_file_name}\n")

                for name, version in package_map.items():
                    # Arbitrary vertical whitespace comes out at as emptystring, so ignore it
                    if name == "":
                        continue

                    f.write(f"{version}\n")


def install_dependencies(*args, dev=False):
    """
    Installs/upgrades Python dependencies for the backend, and places them in
    the appropriate production or dev requirements files.

    :param args: The packages to install
    :type args: str
    :param dev: Specifies if this is a development or production dependency
    :type dev: bool, optional
    """
    initialize_files()
    file_name = dev_file_name if dev else prod_file_name
    with repository_root():
        with use_dir(Projects.BACKEND):
            run([pip, "install", "--upgrade", *args])
            freeze_map = packages_to_map(freeze())

            with open(file_name) as f:
                file_map = packages_to_map(f.read().split("\n"))

            for name in args:
                file_map[name] = freeze_map[name]

            dump_dependencies(file_map, dev=dev)


def initialize_files():
    with repository_root():
        with use_dir(Projects.BACKEND):
            if not os.path.exists(prod_file_name):
                open(prod_file_name, "w").close()

            if not os.path.exists(dev_file_name):
                open(dev_file_name, "w").close()
