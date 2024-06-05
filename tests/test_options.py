# ******************************************************************************
#
# django-loader, a configuration and secret loader for Django
#
# Copyright 2021-2024 Jeremy A Gray <gray@flyquackswim.com>.
#
# SPDX-License-Identifier: MIT
#
# ******************************************************************************

"""django-loader command line options tests."""

import pytest

import djangosecretsloader as DSL


def test_default_arguments(capsys):
    """Should dump default arguments."""
    with pytest.raises(SystemExit):
        DSL.main(["-D", "MY_VAR", "arguments"])

        assert 'MY_VAR = "arguments"' in capsys.readouterr().out

    with pytest.raises(SystemExit):
        DSL.main(["-D", "MY_VAR", "arguments", "-d", "TOML"])

        assert 'MY_VAR = "arguments"' in capsys.readouterr().out

    with pytest.raises(SystemExit):
        DSL.main(["-D", "MY_VAR", "arguments", "-d", "JSON"])

        assert '"MY_VAR": "arguments"' in capsys.readouterr().out

    with pytest.raises(SystemExit):
        DSL.main(["-D", "MY_VAR", "arguments", "-d", "YAML"])

        assert 'MY_VAR = "arguments"' in capsys.readouterr().out

    with pytest.raises(SystemExit):
        DSL.main(["-D", "MY_VAR", "arguments", "-d", "BespON"])

        assert 'MY_VAR = "arguments"' in capsys.readouterr().out

    with pytest.raises(SystemExit):
        DSL.main(["-D", "MY_VAR", "arguments", "-d", "ENV"])

        assert 'MY_VAR="arguments"' in capsys.readouterr().out


def test_file_default_arguments(fs, capsys):
    """Should dump file and default arguments."""
    # Create a secrets file.
    fn = ".env"
    fs.create_file(fn)
    with open(fn, "w") as file:
        file.write(
            r"""TEST_VAR = "file"
TEST_VAR2 = "two"
"""
        )

    with pytest.raises(SystemExit):
        DSL.main(["-D", "TEST_VAR", "arguments", "-f", ".env"])

        assert 'TEST_VAR = "file"' in capsys.readouterr().out


def test_environment_default_arguments(monkeypatch, capsys):
    """Should dump environment and default arguments."""
    # Create the environment variable.
    monkeypatch.setenv("DJANGO_ENV_TEST_VAR", "environment")

    with pytest.raises(SystemExit):
        DSL.main(["-D", "TEST_VAR", "arguments"])

        assert 'TEST_VAR = "environment"' in capsys.readouterr().out


def test_generate_secret_key(capsys):
    """Should exit with a 0 return value."""
    with pytest.raises(SystemExit) as error:
        DSL.main(["-g"])

        assert len(capsys.readouterr().out().strip()) == 50
        assert str(error.value) == "0"

    with pytest.raises(SystemExit) as error:
        DSL.main(["--generate"])

        assert len(capsys.readouterr().out().strip()) == 50
        assert str(error.value) == "0"


def test_validate_secrets_good_file(fs):
    """Should exit with a 0 return value.."""
    fn = ".env"
    fs.create_file(fn)
    with open(fn, "w") as file:
        file.write("a = 1")

    with pytest.raises(SystemExit) as error:
        DSL.main(["-V"])

    assert str(error.value) == "0"

    with pytest.raises(SystemExit) as error:
        DSL.main(["--validate-secrets"])

    assert str(error.value) == "0"


def test_validate_secrets_bad_file(fs):
    """Should exit with a 0 return value.."""
    fn = ".env"
    fs.create_file(fn)
    with open(fn, "w") as file:
        file.write("{ blah ]")

    with pytest.raises(SystemExit) as error:
        DSL.main(["-V"])

    assert str(error.value) == "1"


def test_show_license_info(capsys):
    """Should show license and warranty."""
    expected = """\
django-loader, a configuration and secret loader for Django

MIT License

Copyright (c) 2021-2024 Jeremy A Gray <gray@flyquackswim.com>.

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
        DSL.main(["--show-license"])

        actual = capsys.readouterr().out

        assert actual == expected

    with pytest.raises(SystemExit):
        DSL.main(["--show-warranty"])

        actual = capsys.readouterr().out

        assert actual == expected
