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

.. autofunction:: djangosecretsloader.generate_secret_key
.. autofunction:: djangosecretsloader.load_secrets
.. autofunction:: djangosecretsloader.dump_secrets
.. autofunction:: djangosecretsloader.main

Private
=======

These functions are utility functions and their implementations and
interfaces may change at any time.

.. autofunction:: djangosecretsloader._convert_dict_to_list
.. autofunction:: djangosecretsloader._convert_listdict_to_list
.. autofunction:: djangosecretsloader._dump_secrets_environment
.. autofunction:: djangosecretsloader._keys_are_indices
.. autofunction:: djangosecretsloader._load_secrets_environment
.. autofunction:: djangosecretsloader._load_secrets_file
.. autofunction:: djangosecretsloader._merge
.. autofunction:: djangosecretsloader._validate_file_format
