Advanced Usage
==============

.. toctree::
  :maxdepth: 2

  components
  utils/index

How Zygoat Generators are Structured
------------------------------------

A ``zygoat`` project generator consists of a set of components, which can be arbitrarily nested. ``zygoat`` provides a set of utility classes that cover common use cases for various components. The main two are the base ``Component`` class and the ``FileComponent`` class for copying files from a resource package to the generated project.

``zygoat`` also provides a ``SettingsComponent`` that uses ``redbaron`` to allow you to programmatically modify Python files, mostly used for updating Django settings during project creation.
