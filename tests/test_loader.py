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
def test_load_file_nonexistent_no_raise():
    """Should return an empty dict with no file."""
    actual = loader.load_file("not_a_file", raise_bad_format=False)
    expected = {}

    assert actual == expected


def test_load_file_nonexistent_raise():
    """Should return an empty dict with no file."""
    actual = loader.load_file("not_a_file", raise_bad_format=True)
    expected = {}

    assert actual == expected

    actual = loader.load_file("not_a_file")
    expected = {}

    assert actual == expected


def test_load_file_nonexistent_warn():
    """Should warn on non-existent file."""
    with pytest.warns(UserWarning):
        loader.load_file("not_a_file")


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
        file.write("|=== one\ntwo = three\n|===/\n")

    actual = loader.load_file(fn)
    expected = {
        "one": {
            "two": "three",
        },
    }

    assert actual == expected


def test_load_bad_format_raise(fs):
    """Should raise ``ImproperlyConfigured`` on bad file format."""
    # Need a fake file here.
    fn = ".env"
    fs.create_file(fn)
    with open(fn, "w") as file:
        file.write("{{yaml:sucks}}")

    with pytest.raises(ImproperlyConfigured):
        loader.load_file(fn)

    with pytest.raises(ImproperlyConfigured):
        loader.load_file(fn, raise_bad_format=True)


def test_load_bad_format_no_raise(fs):
    """Should return an empty dict on bad file format."""
    # Need a fake file here.
    fn = ".env"
    fs.create_file(fn)
    with open(fn, "w") as file:
        file.write("{{yaml:sucks}}")

    actual = loader.load_file(fn, raise_bad_format=False)
    expected = {}

    assert actual == expected


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
    """Should load environment dict with default prefix."""
    monkeypatch.setenv("DJANGO_ENV_TEST_VAR", "test")
    expected = {
        "TEST_VAR": "test",
    }
    actual = loader.load_environment()

    assert actual == expected


def test_load_environment_prefix(monkeypatch):
    """Should load environment dict with custom prefix."""
    monkeypatch.setenv("MY_APP_PREFIX_TEST_VAR", "test")
    expected = {
        "TEST_VAR": "test",
    }
    actual = loader.load_environment(prefix="MY_APP_PREFIX_")

    assert actual == expected


def test_load_environment_no_prefix(monkeypatch):
    """Should load empty dict with unprefixed variables."""
    monkeypatch.setenv("TEST_VAR", "test")
    expected = {}
    actual = loader.load_environment()

    assert actual == expected


def test_load_environment_missing():
    """Should load empty dict with no environment variables."""
    expected = {}
    actual = loader.load_environment()

    assert actual == expected


def test_load_list(monkeypatch):
    """Should load list with list-style environment variables."""
    monkeypatch.setenv("DJANGO_ENV_FRUIT__0", "apple")
    monkeypatch.setenv("DJANGO_ENV_FRUIT__1", "banana")
    monkeypatch.setenv("DJANGO_ENV_FRUIT__2", "orange")
    expected = {
        "FRUIT": [
            "apple",
            "banana",
            "orange",
        ],
    }
    actual = loader.load_environment()

    assert actual == expected


def test_load_nested_list(monkeypatch):
    """Should load nested list with list-style environment variables."""
    monkeypatch.setenv("DJANGO_ENV_FOOD__FRUIT__0", "apple")
    monkeypatch.setenv("DJANGO_ENV_FOOD__FRUIT__1", "banana")
    monkeypatch.setenv("DJANGO_ENV_FOOD__FRUIT__2", "orange")
    expected = {
        "FOOD": {
            "FRUIT": [
                "apple",
                "banana",
                "orange",
            ],
        },
    }
    actual = loader.load_environment()

    assert actual == expected


def test_load_dict(monkeypatch):
    """Should load dict with dict-style environment variables."""
    monkeypatch.setenv("DJANGO_ENV_FRUIT__APPLE", "2")
    monkeypatch.setenv("DJANGO_ENV_FRUIT__BANANA", "3")
    monkeypatch.setenv("DJANGO_ENV_FRUIT__ORANGE", "5")
    expected = {
        "FRUIT": {
            "APPLE": "2",
            "BANANA": "3",
            "ORANGE": "5",
        },
    }
    actual = loader.load_environment()

    assert actual == expected


def test_load_nested_dict(monkeypatch):
    """Should load nested dict with dict-style environment variables."""
    monkeypatch.setenv("DJANGO_ENV_FOOD__FRUIT__APPLE", "2")
    monkeypatch.setenv("DJANGO_ENV_FOOD__FRUIT__BANANA", "3")
    monkeypatch.setenv("DJANGO_ENV_FOOD__FRUIT__ORANGE", "5")
    expected = {
        "FOOD": {
            "FRUIT": {
                "APPLE": "2",
                "BANANA": "3",
                "ORANGE": "5",
            },
        },
    }
    actual = loader.load_environment()

    assert actual == expected


def test_load_mixed(monkeypatch):
    """Should load all styles of environment variables mixed."""
    monkeypatch.setenv("DJANGO_ENV_BREAKFAST", "toast")
    monkeypatch.setenv("DJANGO_ENV_FRUITLIST__0", "apple")
    monkeypatch.setenv("DJANGO_ENV_FRUITLIST__1", "banana")
    monkeypatch.setenv("DJANGO_ENV_FRUITLIST__2", "orange")
    monkeypatch.setenv("DJANGO_ENV_FOOD__FRUITLIST__0", "apple")
    monkeypatch.setenv("DJANGO_ENV_FOOD__FRUITLIST__1", "banana")
    monkeypatch.setenv("DJANGO_ENV_FOOD__FRUITLIST__2", "orange")
    monkeypatch.setenv("DJANGO_ENV_FRUIT__APPLE", "2")
    monkeypatch.setenv("DJANGO_ENV_FRUIT__BANANA", "3")
    monkeypatch.setenv("DJANGO_ENV_FRUIT__ORANGE", "5")
    monkeypatch.setenv("DJANGO_ENV_FOOD__FRUIT__APPLE", "2")
    monkeypatch.setenv("DJANGO_ENV_FOOD__FRUIT__BANANA", "3")
    monkeypatch.setenv("DJANGO_ENV_FOOD__FRUIT__ORANGE", "5")
    expected = {
        "BREAKFAST": "toast",
        "FRUITLIST": [
            "apple",
            "banana",
            "orange",
        ],
        "FRUIT": {
            "APPLE": "2",
            "BANANA": "3",
            "ORANGE": "5",
        },
        "FOOD": {
            "FRUITLIST": [
                "apple",
                "banana",
                "orange",
            ],
            "FRUIT": {
                "APPLE": "2",
                "BANANA": "3",
                "ORANGE": "5",
            },
        },
    }
    actual = loader.load_environment()

    assert actual == expected


def test_load_mixed_duplicate(monkeypatch):
    """Should load all styles of environment variables mixed."""
    monkeypatch.setenv("DJANGO_ENV_FRUIT", "apple")
    monkeypatch.setenv("DJANGO_ENV_FRUIT__APPLE", "2")
    monkeypatch.setenv("DJANGO_ENV_FRUIT__BANANA", "3")
    monkeypatch.setenv("DJANGO_ENV_FRUIT__ORANGE", "5")

    with pytest.raises(ImproperlyConfigured):
        loader.load_environment()


def test_dump_mixed(monkeypatch):
    """Should load and all styles of environment variables mixed."""
    monkeypatch.setenv("DJANGO_ENV_BREAKFAST", "toast")
    monkeypatch.setenv("DJANGO_ENV_FRUITLIST__0", "apple")
    monkeypatch.setenv("DJANGO_ENV_FRUITLIST__1", "banana")
    monkeypatch.setenv("DJANGO_ENV_FRUITLIST__2", "orange")
    monkeypatch.setenv("DJANGO_ENV_FOOD__FRUITLIST__0", "apple")
    monkeypatch.setenv("DJANGO_ENV_FOOD__FRUITLIST__1", "banana")
    monkeypatch.setenv("DJANGO_ENV_FOOD__FRUITLIST__2", "orange")
    monkeypatch.setenv("DJANGO_ENV_FRUIT__APPLE", "2")
    monkeypatch.setenv("DJANGO_ENV_FRUIT__BANANA", "3")
    monkeypatch.setenv("DJANGO_ENV_FRUIT__ORANGE", "5")
    monkeypatch.setenv("DJANGO_ENV_FOOD__FRUIT__APPLE", "2")
    monkeypatch.setenv("DJANGO_ENV_FOOD__FRUIT__BANANA", "3")
    monkeypatch.setenv("DJANGO_ENV_FOOD__FRUIT__ORANGE", "5")

    expected = """export DJANGO_ENV_BREAKFAST='toast'
export DJANGO_ENV_FRUITLIST_0='apple'
export DJANGO_ENV_FRUITLIST_1='banana'
export DJANGO_ENV_FRUITLIST_2='orange'
export DJANGO_ENV_FRUIT_APPLE='2'
export DJANGO_ENV_FRUIT_BANANA='3'
export DJANGO_ENV_FRUIT_ORANGE='5'
export DJANGO_ENV_FOOD_FRUITLIST_0='apple'
export DJANGO_ENV_FOOD_FRUITLIST_1='banana'
export DJANGO_ENV_FOOD_FRUITLIST_2='orange'
export DJANGO_ENV_FOOD_FRUIT_APPLE='2'
export DJANGO_ENV_FOOD_FRUIT_BANANA='3'
export DJANGO_ENV_FOOD_FRUIT_ORANGE='5'"""

    actual = loader.dump_environment(loader.load_environment())

    assert actual == expected


def test_dump_mixed_no_export(monkeypatch):
    """Should load and all styles of environment variables mixed."""
    monkeypatch.setenv("DJANGO_ENV_BREAKFAST", "toast")
    monkeypatch.setenv("DJANGO_ENV_FRUITLIST__0", "apple")
    monkeypatch.setenv("DJANGO_ENV_FRUITLIST__1", "banana")
    monkeypatch.setenv("DJANGO_ENV_FRUITLIST__2", "orange")
    monkeypatch.setenv("DJANGO_ENV_FOOD__FRUITLIST__0", "apple")
    monkeypatch.setenv("DJANGO_ENV_FOOD__FRUITLIST__1", "banana")
    monkeypatch.setenv("DJANGO_ENV_FOOD__FRUITLIST__2", "orange")
    monkeypatch.setenv("DJANGO_ENV_FRUIT__APPLE", "2")
    monkeypatch.setenv("DJANGO_ENV_FRUIT__BANANA", "3")
    monkeypatch.setenv("DJANGO_ENV_FRUIT__ORANGE", "5")
    monkeypatch.setenv("DJANGO_ENV_FOOD__FRUIT__APPLE", "2")
    monkeypatch.setenv("DJANGO_ENV_FOOD__FRUIT__BANANA", "3")
    monkeypatch.setenv("DJANGO_ENV_FOOD__FRUIT__ORANGE", "5")

    expected = """DJANGO_ENV_BREAKFAST='toast'
DJANGO_ENV_FRUITLIST_0='apple'
DJANGO_ENV_FRUITLIST_1='banana'
DJANGO_ENV_FRUITLIST_2='orange'
DJANGO_ENV_FRUIT_APPLE='2'
DJANGO_ENV_FRUIT_BANANA='3'
DJANGO_ENV_FRUIT_ORANGE='5'
DJANGO_ENV_FOOD_FRUITLIST_0='apple'
DJANGO_ENV_FOOD_FRUITLIST_1='banana'
DJANGO_ENV_FOOD_FRUITLIST_2='orange'
DJANGO_ENV_FOOD_FRUIT_APPLE='2'
DJANGO_ENV_FOOD_FRUIT_BANANA='3'
DJANGO_ENV_FOOD_FRUIT_ORANGE='5'"""

    actual = loader.dump_environment(loader.load_environment(), export=False)

    assert actual == expected


def test_keys_are_indices():
    """Should determine if keys are list indices."""
    # They are indices.
    ds = {
        "0": "apple",
        "1": "banana",
        "2": "orange",
    }

    assert loader._keys_are_indices(ds) is True

    # Non-integer index.
    ds = {
        "zero": "apple",
        "1": "banana",
        "2": "orange",
    }

    # Wrong start.
    ds = {
        "3": "apple",
        "1": "banana",
        "2": "orange",
    }

    assert loader._keys_are_indices(ds) is False

    # Non-sequential.
    ds = {
        "0": "apple",
        "2": "banana",
        "3": "orange",
    }

    assert loader._keys_are_indices(ds) is False


def test_convert_dict_to_list():
    """Should convert dict to list."""
    listdict = {
        "0": "apple",
        "1": "banana",
        "2": "orange",
    }

    expected = [
        "apple",
        "banana",
        "orange",
    ]

    assert loader._convert_dict_to_list(listdict) == expected


def test_convert_listdict_to_list():
    """Should convert list-like dicts to lists in a data structure."""
    listdict = {
        "fruit": {
            "0": "apple",
            "1": "banana",
            "2": "orange",
        },
    }

    expected = {
        "fruit": [
            "apple",
            "banana",
            "orange",
        ],
    }

    assert loader._convert_listdict_to_list(listdict) == expected


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

    expected = "export DJANGO_ENV_SOME_VAR='test'"

    actual = loader.dump_secrets(fmt="ENV", **config)

    assert actual == expected
