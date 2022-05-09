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
"""loader.py tests."""

import sys
from pathlib import Path

import pytest

from django.core.exceptions import ImproperlyConfigured

sys.path.insert(0, "/home/gray/src/work/django-loader")

import loader  # noqa: E402


def test_validate_file_format_raise_no_file():
    """Should raise with no file."""
    # Non-existent file name.
    fn = "not-a-file"

    with pytest.raises(ImproperlyConfigured) as error:
        loader.validate_file_format(fn)

    assert str(error.value) == f"Secrets file {Path(fn).resolve()} does not exist."


def test_validate_file_format_raise_no_format(fs):
    """Should raise with no format."""
    fn = ".env"
    fs.create_file(fn)
    with open(fn, "w") as file:
        file.write("{ blah ]")

    with pytest.raises(ImproperlyConfigured) as error:
        loader.validate_file_format(fn)

    assert (
        str(error.value)
        == f"Configuration file {Path(fn).resolve()} is not a recognized format."
    )


def test_validate_file_format_valid_toml(fs, capsys):
    """Should return ``True``."""
    fn = ".env"
    fs.create_file(fn)
    with open(fn, "w") as file:
        file.write("a = 1")

    assert loader.validate_file_format(fn) is True

    out = capsys.readouterr().out
    assert f"Secrets file {Path(fn).resolve()} recognized as TOML." in out


def test_validate_file_format_valid_json(fs, capsys):
    """Should return ``True``."""
    fn = ".env"
    fs.create_file(fn)

    with open(fn, "w") as file:
        file.write('{"one": "two"}')

    assert loader.validate_file_format(fn) is True

    out = capsys.readouterr().out
    assert "toml error" in out
    assert f"Secrets file {Path(fn).resolve()} not recognized as TOML." in out
    assert f"Secrets file {Path(fn).resolve()} recognized as JSON." in out


def test_validate_file_format_valid_yaml(fs, capsys):
    """Should return ``True``."""
    fn = ".env"
    fs.create_file(fn)

    with open(fn, "w") as file:
        file.write("---\n- name: WCFM deployment\n")

    assert loader.validate_file_format(fn) is True

    out = capsys.readouterr().out
    assert "toml error" in out
    assert f"Secrets file {Path(fn).resolve()} not recognized as TOML." in out
    assert "json error" in out
    assert f"Secrets file {Path(fn).resolve()} not recognized as JSON." in out
    assert f"Secrets file {Path(fn).resolve()} recognized as YAML." in out


def test_validate_file_format_valid_bespon(fs, capsys):
    """Should return ``True``."""
    fn = ".env"
    fs.create_file(fn)

    with open(fn, "w") as file:
        file.write("|=== one\ntwo = three\n|===/\n")

    assert loader.validate_file_format(fn) is True

    out = capsys.readouterr().out
    assert "toml error" in out
    assert f"Secrets file {Path(fn).resolve()} not recognized as TOML." in out
    assert "json error" in out
    assert f"Secrets file {Path(fn).resolve()} not recognized as JSON." in out
    assert "yaml error" in out
    assert f"Secrets file {Path(fn).resolve()} not recognized as YAML." in out
    assert f"Secrets file {Path(fn).resolve()} recognized as BespON." in out
