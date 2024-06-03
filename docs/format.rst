.. *****************************************************************************
..
.. django-loader, a configuration and secret loader for Django
..
.. Copyright 2021-2024 Jeremy A Gray <gray@flyquackswim.com>.
..
.. SPDX-License-Identifier: MIT
..
.. *****************************************************************************

=============================
 Environment Variable Format
=============================

.. toctree::
   :maxdepth: 2

Prefixes
========

``django-loader`` uses a prefix on variable names to separate its
variables from the other variables in the environment.  This defaults
to ``DJANGO_ENV_`` and is user configurable.  This prefix is removed
when the variable is stored as a python dict.

Scalars
=======

Scalars are simply name value pairs.  ``django-loader`` does no type
checking or validation.  The environment variable::

  DJANGO_ENV_MY_SCALAR=value

would be stored in the configuration dictionary as::

  { "MY_SCALAR": "value" }

Names and values are case sensitive, as always.

Dicts
=====

Dictionaries follow the same rules as scalars, but use two underscores
(``__``) to separate keys and values.  Lists and dictionaries are
nestable.  The environment variable::

  DJANGO_ENV_MY_DICT__NAME=jon

would be stored in the configuration dictionary as::

  {"MY_DICT": { "NAME": "jon" }}

Lists
=====

Lists are implemented as dictionaries, but use integer indices as
keys.  Lists and dictionaries are nestable.  The environment
variable::

  DJANGO_ENV_MY_LIST__0=jon

would be stored in the configuration dictionary as::

  { "MY_LIST": ["jon"] }

Indices have to be contiguous and start at 0 or they will be treated
as dictionaries with numerical keys.
