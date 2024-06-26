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
 CLI Arguments
===============

Command line help::

  usage:  [-h] [--show-warranty] [--show-license] [-p PREFIX]
          [-d {TOML,JSON,YAML,BespON,ENV}] [-V] [-g]
          [file]

  This program comes with ABSOLUTELY NO WARRANTY; for details type ``loader.py
  --show-warranty``. This is free software, and you are welcome to redistribute it
  under certain conditions; type ``loader.py --show-license`` for details.

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
    -V, --validate-secrets-format
                          Validate the secrets file format.
    -g, --generate-secret-key
                          Generate a secret key.
