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

Installation
============

Install django-loader with::

  pip install django-loader
  pip freeze > requirements.txt

or add as a poetry dependency.

Usage
=====

Console::

    usage: loader.py [-h] [--show-warranty] [--show-license] [-p PREFIX]
                     [-d {TOML,JSON,YAML,BespON,ENV}] [-V] [-g]
                     [file]

    This program comes with ABSOLUTELY NO WARRANTY; for details type ``loader.py
    --show-warranty``. This is free software, and you are welcome to redistribute
    it under certain conditions; type ``loader.py --show-license`` for details.

    positional arguments:
      file                  Secrets file to be loaded; default is `.env`.

    options:
      -h, --help            show this help message and exit
      --show-warranty       Show warranty information.
      --show-license        Show license information.
      -p PREFIX, --prefix PREFIX
                            Environment variable prefix.
      -d {TOML,JSON,YAML,BespON,ENV}, --dump-format {TOML,JSON,YAML,BespON,ENV}
                            Configuration dump format.
      -V, --validate-secrets
                            Validate the secrets only.
      -g, --generate-secret-key
                            Generate a secret key.

In Python::

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

Copyright (C) 2021-2022 `Jeremy A Gray <gray@flyquackswim.com>`_.

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
