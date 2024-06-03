.. *****************************************************************************
..
.. django-loader, a configuration and secret loader for Django
..
.. Copyright 2021-2024 Jeremy A Gray <gray@flyquackswim.com>.
..
.. SPDX-License-Identifier: MIT
..
.. *****************************************************************************

===========
 Functions
===========

.. toctree::
   :maxdepth: 2

Public
======

These functions form the exposed API and can be relied on to change
only as implied by the semantic version of the package.

.. autofunction:: loader.generate_secret_key
.. autofunction:: loader.load_secrets
.. autofunction:: loader.dump_secrets
.. autofunction:: loader.main

Private
=======

These functions are utility functions and their implementations and
interfaces may change at any time.

.. autofunction:: loader._convert_dict_to_list
.. autofunction:: loader._convert_listdict_to_list
.. autofunction:: loader._dump_secrets_environment
.. autofunction:: loader._keys_are_indices
.. autofunction:: loader._load_secrets_environment
.. autofunction:: loader._load_secrets_file
.. autofunction:: loader._merge
.. autofunction:: loader._validate_file_format
