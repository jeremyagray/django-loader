# ******************************************************************************
#
# django-loader, a configuration and secret loader for Django
#
# test_loader.py:  tests for loader.py
#
# Copyright (C) 2021 Jeremy A Gray <gray@flyquackswim.com>.
#
# SPDX-License-Identifier: MIT
#
# ******************************************************************************
#
"""loader.py tests."""

import sys

import pytest

from django.core.exceptions import ImproperlyConfigured

sys.path.insert(0, "/home/gray/src/work/django-loader")

import loader  # noqa: E402


# loader.merge() tests.
def test_merge_empty_defaults():
    """Should return an empty dict with empty defaults."""
    defaults = {}
    file = {}
    env = {}

    actual = loader.merge(defaults, file, env)
    expected = {}

    assert actual == expected

    file = {
        "SOME_VAR": "test",
    }
    env = {}

    actual = loader.merge(defaults, file, env)
    expected = {}

    assert actual == expected

    file = {}
    env = {
        "SOME_VAR": "test",
    }

    actual = loader.merge(defaults, file, env)
    expected = {}

    assert actual == expected

    file = {
        "SOME_VAR": "test",
    }
    env = {
        "OTHER_VAR": "test",
    }

    actual = loader.merge(defaults, file, env)
    expected = {}

    assert actual == expected


def test_merge_one_default():
    """Should return a single entry dict."""
    defaults = {
        "SOME_VAR": "defaults",
    }
    file = {}
    env = {}

    actual = loader.merge(defaults, file, env)
    expected = defaults

    assert actual == expected

    file = {
        "SOME_VAR": "file",
    }
    env = {}

    actual = loader.merge(defaults, file, env)
    expected = file

    assert actual == expected

    env = {
        "SOME_VAR": "env",
    }

    actual = loader.merge(defaults, file, env)
    expected = env

    assert actual == expected

    file = {
        "SOME_VAR": "file",
    }
    env = {
        "OTHER_VAR": "env",
    }

    actual = loader.merge(defaults, file, env)
    expected = file

    assert actual == expected

    file = {
        "OTHER_VAR": "file",
    }
    env = {
        "SOME_VAR": "env",
    }

    actual = loader.merge(defaults, file, env)
    expected = env

    assert actual == expected

    file = {
        "SOME_VAR": "file",
        "OTHER_VAR": "file",
    }
    env = {
        "SOME_VAR": "env",
        "OTHER_VAR": "env",
    }

    actual = loader.merge(defaults, file, env)
    expected = {
        "SOME_VAR": "env",
    }

    assert actual == expected


# loader.load_file() tests.
def test_load_file_nonexistent():
    """Should return an empty dict with no file."""
    actual = loader.load_file("not_a_file")
    expected = {}

    assert actual == expected


def test_load_file_valid_toml(fs):
    """Should return a dict from valid TOML."""
    # Need a fake file here.
    fn = ".env"
    fs.create_file(fn)
    with open(fn, "w") as file:
        file.write('SOME_VAR = "this is TOML"')

    actual = loader.load_file(fn)
    expected = {
        "SOME_VAR": "this is TOML",
    }

    assert actual == expected


def test_load_file_valid_json(fs):
    """Should return a dict from valid JSON."""
    # Need a fake file here.
    fn = ".env"
    fs.create_file(fn)
    with open(fn, "w") as file:
        file.write('{\n  "SOME_VAR": "this is JSON"\n}')

    actual = loader.load_file(fn)
    expected = {
        "SOME_VAR": "this is JSON",
    }

    assert actual == expected


def test_load_file_valid_yaml(fs):
    """Should return a dict from valid YAML."""
    # Need a fake file here.
    fn = ".env"
    fs.create_file(fn)
    with open(fn, "w") as file:
        file.write("SOME_VAR: this is YAML")

    actual = loader.load_file(fn)
    expected = {
        "SOME_VAR": "this is YAML",
    }

    assert actual == expected


def test_load_file_valid_bespon(fs):
    """Should return a dict from valid BespON."""
    # Need a fake file here.
    fn = ".env"
    fs.create_file(fn)
    with open(fn, "w") as file:
        file.write('SOME_VAR = "this is BespON"')

    actual = loader.load_file(fn)
    expected = {
        "SOME_VAR": "this is BespON",
    }

    assert actual == expected


def test_load_bad_format_no_raise(fs):
    """Should return an empty dict on bad file format."""
    # Need a fake file here.
    fn = ".env"
    fs.create_file(fn)
    with open(fn, "w") as file:
        file.write("{{yaml:sucks}}")

    actual = loader.load_file(fn)
    expected = {}

    assert actual == expected


def test_load_bad_format_raise(fs):
    """Should raise ``ImproperlyConfigured`` on bad file format."""
    # Need a fake file here.
    fn = ".env"
    fs.create_file(fn)
    with open(fn, "w") as file:
        file.write("{{yaml:sucks}}")

    with pytest.raises(ImproperlyConfigured):
        loader.load_file(fn, raise_bad_format=True)


# loader.generate_secret_key() tests.
def test_generate_secret_key_generates_key():
    """Test key generation."""
    actual = loader.generate_secret_key()

    assert actual != ""
    assert len(actual) == 50


def test_generate_secret_key_length():
    """Test generated key length."""
    actual = loader.generate_secret_key()

    assert len(actual) == 50


def test_generate_secret_key_successive_keys_different():
    """Test that successive keys are different."""
    one = loader.generate_secret_key()
    two = loader.generate_secret_key()

    assert one != two


# loader.validate_not_empty_string() tests.
def test_validate_not_empty_string_string():
    """Should return ``True`` on a string."""
    name = "NON_EMPTY_STRING"
    val = "string"

    assert loader.validate_not_empty_string(name, val) is True


def test_validate_not_empty_string_empty_string():
    """Should raise exception on an empty string."""
    name = "EMPTY_STRING"
    val = ""

    with pytest.raises(ImproperlyConfigured):
        loader.validate_not_empty_string(name, val)


# loader.validate_falsy() tests.
def test_validate_falsy_falsy_values():
    """Should return ``True`` for falsy values."""
    name = "FALSY_VALUE"
    values = [
        False,
        None,
        "",
        0,
        0x0,
        0o0,
        0.0,
        [],
        {},
    ]

    for val in values:
        assert loader.validate_falsy(name, val) is True


def test_validate_falsy_truthy_values():
    """Should raise an exception for truthy values."""
    name = "FALSY_VALUE"
    values = [
        True,
        "hi",
        1,
        0x1,
        0o1,
        0.1,
        ["hi"],
        {"hi": "lois"},
    ]

    for val in values:
        with pytest.raises(ImproperlyConfigured):
            loader.validate_falsy(name, val)


# loader.validate_truthy() tests.
def test_validate_truthy_falsy_values():
    """Should raise an exception for falsy values."""
    name = "TRUTHY_VALUE"
    values = [
        False,
        None,
        "",
        0,
        0x0,
        0o0,
        0.0,
        [],
        {},
    ]

    for val in values:
        with pytest.raises(ImproperlyConfigured):
            loader.validate_truthy(name, val)


def test_validate_truthy_truthy_values():
    """Should return ``True`` for truthy values."""
    name = "TRUTHY_VALUE"
    values = [
        True,
        "hi",
        1,
        0x1,
        0o1,
        0.1,
        ["hi"],
        {"hi": "lois"},
    ]

    for val in values:
        assert loader.validate_truthy(name, val) is True


# loader.load_environment() tests.
def test_load_environment(monkeypatch):
    """Test load_environment()."""
    monkeypatch.setenv("DJANGO_ENV_TEST_VAR", "test")
    expected = {
        "TEST_VAR": "test",
    }
    actual = loader.load_environment()

    assert actual == expected


def test_load_environment_prefix(monkeypatch):
    """Test load_environment() with a custom prefix."""
    monkeypatch.setenv("MY_APP_PREFIX_TEST_VAR", "test")
    expected = {
        "TEST_VAR": "test",
    }
    actual = loader.load_environment(prefix="MY_APP_PREFIX_")

    assert actual == expected


def test_load_environment_no_prefix(monkeypatch):
    """Test load_environment() with variable missing prefix."""
    monkeypatch.setenv("TEST_VAR", "test")
    expected = {}
    actual = loader.load_environment()

    assert actual == expected


def test_load_environment_missing():
    """Test load_environment() with no variables."""
    expected = {}
    actual = loader.load_environment()

    assert actual == expected


# loader.load_secrets() tests.
def test_load_secrets(fs, monkeypatch):
    """Should load the correct secrets dict."""
    # Set the defaults.
    defaults = {
        "TEST_VAR": "defaults",
    }

    # Set the file.
    fn = ".env"
    fs.create_file(fn)
    with open(fn, "w") as file:
        file.write('TEST_VAR = "file"')

    # Set the environment.
    monkeypatch.setenv("DJANGO_ENV_TEST_VAR", "env")

    expected = {
        "TEST_VAR": "env",
    }

    actual = loader.load_secrets(**defaults)

    assert actual == expected


# loader.dump_secrets() tests.
def test_dump_secrets_toml():
    """Should dump valid TOML."""
    config = {
        "SOME_VAR": "test",
    }

    actual = loader.dump_secrets(**config)
    expected = 'SOME_VAR = "test"\n'

    assert actual == expected


def test_dump_secrets_json():
    """Should dump valid JSON."""
    config = {
        "SOME_VAR": "test",
    }

    actual = loader.dump_secrets(fmt="JSON", **config)
    expected = '{"SOME_VAR": "test"}'

    assert actual == expected


def test_dump_secrets_yaml():
    """Should dump valid YAML."""
    config = {
        "SOME_VAR": "test",
    }

    actual = loader.dump_secrets(fmt="YAML", **config)
    expected = "{SOME_VAR: test}\n"

    assert actual == expected


def test_dump_secrets_bespon():
    """Should dump valid BespON."""
    config = {
        "SOME_VAR": "test",
    }

    actual = loader.dump_secrets(fmt="BespON", **config)
    expected = "SOME_VAR = test\n"

    assert actual == expected


def test_dump_secrets_env():
    """Should raise ``NotImplementedError``."""
    config = {
        "SOME_VAR": "test",
    }

    with pytest.raises(NotImplementedError):
        loader.dump_secrets(fmt="ENV", **config)
