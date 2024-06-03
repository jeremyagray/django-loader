.. *****************************************************************************
..
.. django-loader, a configuration and secret loader for Django
..
.. Copyright 2021-2024 Jeremy A Gray <gray@flyquackswim.com>.
..
.. SPDX-License-Identifier: MIT
..
.. *****************************************************************************

===============
 django-loader
===============

django-loader: a configuration variable and secrets loader for Django
apps.

.. image:: https://badge.fury.io/py/django-loader.svg
   :target: https://badge.fury.io/py/django-loader
   :alt: PyPI Version
.. image:: https://readthedocs.org/projects/django-loader/badge/?version=latest
   :target: https://django-loader.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

What is django-loader?
======================

django-loader is a configuration variable and secrets loader for
Django apps.  It loads a dictionary of configuration variables into
``settings.py`` that consists of default values, values from a secrets
file (defaults to ``.env``), and from environment variables.  It can
load configuration files in TOML, JSON, YAML, and BespON formats and
dump in any format, including as environment variables (Bourne shell).

See the environment variable format specification for more details
about passing environment variables.

Installation
============

Install django-loader with::

  pip install django-loader

or::

  poetry add django-loader

Usage
=====

  >>> import loader
  >>> secrets = loader.load_secrets(**{"SECRET_KEY": ""})
  >>> SECRET_KEY = secrets["SECRET_KEY"]

See the source and `documentation
<https://django-loader.readthedocs.io/en/latest/>`_ for more
information.

Copyright and License
=====================

SPDX-License-Identifier: `MIT <https://spdx.org/licenses/MTI.html>`_

django-loader: a configuration variable and secrets loader for Django
apps.

Copyright (C) 2021-2024 `Jeremy A Gray <gray@flyquackswim.com>`_.

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Author
======

`Jeremy A Gray <gray@flyquackswim.com>`_
