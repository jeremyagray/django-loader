# ******************************************************************************
#
# django-loader, a configuration and secret loader for Django
#
# Copyright 2021-2022 Jeremy A Gray <gray@flyquackswim.com>.
#
# SPDX-License-Identifier: MIT
#
# ******************************************************************************
#
"""loader.py options tests."""

import sys

import pytest

from django.core.exceptions import ImproperlyConfigured

sys.path.insert(0, "/home/gray/src/work/django-loader")

import loader  # noqa: E402


def test_generate_secret_key():
    """Should exit with a 0 return value.."""
    with pytest.raises(SystemExit) as error:
        loader.main(["-g"])

    assert str(error.value) == "0"

    with pytest.raises(SystemExit) as error:
        loader.main(["--generate"])

    assert str(error.value) == "0"


def test_validate_secrets_good_file(fs):
    """Should exit with a 0 return value.."""
    fn = ".env"
    fs.create_file(fn)
    with open(fn, "w") as file:
        file.write("a = 1")

    with pytest.raises(SystemExit) as error:
        loader.main(["-V"])

    assert str(error.value) == "0"

    with pytest.raises(SystemExit) as error:
        loader.main(["--validate-secrets"])

    assert str(error.value) == "0"


def test_validate_secrets_bad_file(fs):
    """Should exit with a 0 return value.."""
    fn = ".env"
    fs.create_file(fn)
    with open(fn, "w") as file:
        file.write("{ blah ]")

    with pytest.raises(SystemExit) as error:
        loader.main(["-V"])

    assert str(error.value) == "1"


def test_show_license_info(capsys):
    """Should show license and warranty."""
    expected = """\
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

    with pytest.raises(SystemExit):
        loader.main(["--show-license"])

        actual = capsys.readouterr().out

        assert actual == expected

    with pytest.raises(SystemExit):
        loader.main(["--show-warranty"])

        actual = capsys.readouterr().out

        assert actual == expected
