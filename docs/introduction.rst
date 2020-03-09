Getting Started
===============


What is Zygoat?
---------------

``zygoat`` is a tool for creating ``NextJS``/``Django``/``PostgreSQL`` applications. It comes preloaded with a set of project components for spawning a fully functional application, including the deployment stack and docker development configuration.

``zygoat`` can also be used to create your own project generation tools, using a set of well-defined and arbitrarily nested components.


Installation
------------

From ``pypi``

::

   pip install --user zygoat

This adds the ``zg`` executable to your path, which allows you to interact with ``zygoat``'s pre-existing project configuration.


Usage
-----
::

   Usage: zg [OPTIONS] COMMAND [ARGS]...

   Options:
   -v, --verbose
   --help         Show this message and exit.

   Commands:
   create  Create components without initializing a new project
   delete  Calls the delete phase on all included build components
   init    Creates a new zygoat settings file and exits
   list    Lists all of the running phase names
   new     Creates a new settings file and all components
   update  Calls the update phase on all included build components
