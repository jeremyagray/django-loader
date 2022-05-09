# ******************************************************************************
#
# django-loader, a configuration and secret loader for Django
#
# Copyright 2022 Jeremy A Gray <gray@flyquackswim.com>.
#
# SPDX-License-Identifier: MIT
#
# ******************************************************************************
#
"""django-loader command-line options."""

import argparse
import sys
import textwrap


def _create_argument_parser():
    """Create an argparse argument parser."""
    parser = argparse.ArgumentParser(
        description="""\
This program comes with ABSOLUTELY NO WARRANTY; for details type
``loader.py --show-warranty``.  This is free software, and you are welcome
to redistribute it under certain conditions; type ``loader.py
--show-license`` for details.
""",
    )

    parser.add_argument(
        "--show-warranty",
        nargs=0,
        action=_ShowLicenseAction,
        help="Show warranty information.",
    )

    parser.add_argument(
        "--show-license",
        nargs=0,
        action=_ShowLicenseAction,
        help="Show license information.",
    )

    parser.add_argument(
        "-V",
        "--validate-secrets",
        dest="validate_secrets",
        default=False,
        action="store_true",
        help="Validate the secrets only.",
    )

    parser.add_argument(
        "-g",
        "--generate-secret-key",
        dest="generate_secret_key",
        default=False,
        action="store_true",
        help="Generate a secret key.",
    )

    return parser


class _ShowLicenseAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        license = """\
django-loader, a configuration and secret loader for Django

MIT License

Copyright (c) 2021-2022 Jeremy A Gray <gray@flyquackswim.com>.

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
"""
        print(
            "\n\n".join(
                list(
                    map(
                        lambda item: "\n".join(textwrap.wrap(item.strip(), 72)),
                        textwrap.dedent(license).strip().split("\n\n"),
                    )
                )
            )
        )

        sys.exit(0)


def _field_list_handler(s):
    if len(s) == 0:
        return []
    else:
        return [item.strip() for item in s.split(",")]
