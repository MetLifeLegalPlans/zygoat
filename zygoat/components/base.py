from functools import partial
import logging

from click import style

from zygoat.utils.files import repository_root
from zygoat.config import Config
from zygoat.constants import Phases

log = logging.getLogger()


class Component:
    """
    The basic unit of project generation in Zygoat.

    Defines lifecycle hooks and handling for configuration + sub-components.
    """

    def __init__(self, parent=None, sub_components=[]):
        """
        Initializes a new component, loads the configuration, and sets the identifier for sub-components.

        :param sub_components:
            Smaller components that make up individual units of this, for organizational distinction.
        :type sub_components: list, optional
        :param parent:
            The "Django ORM"-esque string that identifies the parent component. Usually ``parent.identifier``.

            Set automatically on ``reload`` - **do not manually specify this**.
        :type parent: str, optional
        """
        self.sub_components = []

        self.reload()
        self.parent = parent

        for component in sub_components:
            component.parent = self.identifier
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

        (i.e. ``Backend__Linting``, ``Backend__Dockerfile``, ``Frontend__Tests``, etc.)
        """
        if self.parent is None:
            return self.name

        return f"{self.parent}__{self.name}"

    @property
    def exclude(self):
        """
        Whether or not this sub-component should be used in the project
        """
        if self.config.get("exclude", None) is None:
            return False

        return self.identifier in self.config.exclude

    @property
    def include(self):
        """
        Convenience wrapper for easier reading
        """
        return not self.exclude

    def call_phase(self, phase, force_create=False):
        """
        Calls a phase function on self + all sub-components.

        If a component does not have the requested phase, it still executes all sub-components.

        :param phase: The phase to run, from ``zygoat.constants.Phases``
        :type phase: str

        :param force_create: Re-run the ``create`` phase even if the component is installed
        :type force_create: bool, optional
        """
        if self.exclude:
            log.debug(f"Skipping {self.identifier} as it was found in the exclude list")
            return

        self.reload()

        run_self = partial(self._run_self, phase, force_create=force_create)
        run_children = partial(self._run_children, phase)

        if phase == Phases.DELETE:
            run_children()
            run_self()
        else:
            run_self()

            # Don't echo force_create events down the tree
            if not force_create:
                run_children()

    @property
    def _log_string(self):
        return "Calling phase {} for {}"

    def _run_self(self, phase, force_create=False):
        phase_func = getattr(self, phase, None)
        is_create = phase == Phases.CREATE
        styled_name = style(self.identifier, bold=True, fg="cyan")

        if phase_func is not None:
            with repository_root():
                if not is_create and not self.installed:
                    log.warning(f"Component {styled_name} is not installed, skipping")
                    return

                if is_create and self.installed and not force_create:
                    log.warning(f"Component {styled_name} is already installed, skipping")
                    return

                log.debug(self._log_string.format(phase, self.__class__.__name__))
                phase_func()

    def _run_children(self, phase):
        for component in self.sub_components:
            log.debug(self._log_string.format(phase, component.__class__.__name__))
            component.call_phase(phase)

    @property
    def installed(self):
        """
        Halts the create phase if True
        """
        return False

    def list(self):
        """
        Prints the identifier of this component for exclusion filtering
        """
        if self.include:
            print(self.identifier)

    def reload(self):
        """
        Reloads the configuration file
        """
        self.config = Config()

        for component in self.sub_components:
            component.parent = self.identifier
