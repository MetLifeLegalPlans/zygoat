Components
==========

.. toctree::
   :maxdepth: 2

   base
   included

What is a component?
--------------------

A component is any well structured Python object that implements any out of a set of lifecycle hooks. These hooks are as follows:

 - ``create`` - installs the component from a completely blank state
 - ``update`` - if the component has been changed in the generator since the project was created, this hook will bring it up to date
 - ``delete`` - removes the component from the project
 - ``deploy`` - what needs to be done to send this component to production
   - Typically this is only implemented on the top level components like ``Frontend`` and ``Backend``, but is available recursively
 - ``list`` - prints out the component's unique identifier, for excluding in the config file

A component also contains a method with signature ``call_phase(phase, force_create=False)`` which will run the phase on this component and all sub components. If the phase is not defined, it moves on to the sub components instead.

**Note:** When running the ``delete`` phase, sub-components are called first followed by self. In addition, components should be run in reverse at the top level and are in the default project.

You should never need to override the base implementation of ``call_phase``, but if you do, ensure that you maintain that minimum standard of functionality.
