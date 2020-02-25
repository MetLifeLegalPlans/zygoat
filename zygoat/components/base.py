import logging

from zygoat.utils.files import repository_root
from zygoat.config import Config

log = logging.getLogger()


class Component:
    def __init__(self, parent=None, sub_components=[]):
        self.config = Config()
        self.parent = parent

        self.sub_components = []

        for component in sub_components:
            component.parent = self.name
            self.sub_components.append(component)

    @property
    def name(self):
        """
        Convenience function for retrieving the class name
        """
        return self.__class__.__name__

    @property
    def identifier(self):
        """
        The component's path in the tree, using django notation

        (i.e. Backend__Linting, Backend__Dockerfile, Frontend__Tests, etc.)
        """
        if self.parent is None:
            return self.name

        return '{self.parent}__{self.name}'

    @property
    def exclude(self):
        """
        Whether or not this sub-component should be used in the project
        """
        if self.config.get('exclude', None) is None:
            return False

        return self.identifier in self.config.exclude

    @property
    def include(self):
        """
        Convenience wrapper for easier reading
        """
        return not self.exclude

    def call_phase(self, phase):
        """
        Calls a phase (e.g. create, update, delete) on self + all sub components
        """
        if self.exclude:
            log.debug(f'Skipping {self.identifier} as it was found in the exclude list')
            return

        log_string = 'Calling phase {} for {}'

        phase_func = getattr(self, phase, None)

        if phase_func is not None:
            with repository_root():
                log.info(log_string.format(phase, self.__class__.__name__))
                phase_func()

        for component in self.sub_components:
            log.info(log_string.format(phase, component.__class__.__name__))
            component.call_phase(phase)
