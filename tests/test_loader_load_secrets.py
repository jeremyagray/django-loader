# ******************************************************************************
#
# django-loader, a configuration and secret loader for Django
#
# Copyright 2021-2024 Jeremy A Gray <gray@flyquackswim.com>.
#
# SPDX-License-Identifier: MIT
#
# ******************************************************************************

"""``load_secrets`` tests."""

import djangosecretsloader as DSL


def test_load_secrets_from_defaults(fs):
    """Should load the secrets from the defaults."""
    # Set the defaults.
    defaults = {
        "TEST_VAR": "defaults",
    }

    expected = {
        "TEST_VAR": "defaults",
    }

    actual = DSL.load_secrets(**defaults)

    assert actual == expected


def test_load_secrets_from_default_file(fs):
    """Should load the secrets from the default file."""
    # Set the defaults.
    defaults = {}

    # Create the file.
    fn = ".env"
    fs.create_file(fn)
    with open(fn, "w") as file:
        file.write('TEST_VAR = "file"')

    expected = {
        "TEST_VAR": "file",
    }

    actual = DSL.load_secrets(**defaults)

    assert actual == expected


def test_load_secrets_from_specified_file(fs):
    """Should load the secrets from a specified file."""
    # Set the defaults.
    defaults = {}

    # Create the file.
    fn = ".env.secret"
    fs.create_file(fn)
    with open(fn, "w") as file:
        file.write('TEST_VAR = "secret_file"')

    expected = {
        "TEST_VAR": "secret_file",
    }

    actual = DSL.load_secrets(".env.secret", **defaults)

    assert actual == expected


def test_load_secrets_from_environment_specified_file(fs, monkeypatch):
    """Should load the secrets from a environment specified file."""
    # Set the defaults.
    defaults = {}

    # Create the file and specify it in the environment.
    fn = ".env.secret"
    fs.create_file(fn)
    with open(fn, "w") as file:
        file.write('TEST_VAR = "secret_file"')

    monkeypatch.setenv("DJANGO_LOADER_ENV_FILE", ".env.secret")

    expected = {
        "TEST_VAR": "secret_file",
    }

    actual = DSL.load_secrets(**defaults)

    assert actual == expected


def test_load_secrets_load_nothing(fs):
    """Should load nothing."""
    # Set the defaults.
    defaults = {}

    expected = {}

    actual = DSL.load_secrets(**defaults)

    assert actual == expected


def test_load_secrets_files_overwrite_defaults(fs):
    """Files should overwrite the defaults."""
    # Set the defaults.
    defaults = {
        "TEST_VAR": "defaults",
    }

    # Create the file.
    fn = ".env"
    fs.create_file(fn)
    with open(fn, "w") as file:
        file.write('TEST_VAR = "file"')

    expected = {
        "TEST_VAR": "file",
    }

    actual = DSL.load_secrets(**defaults)

    assert actual == expected


def test_load_secrets_environment_overwrites_defaults(fs, monkeypatch):
    """Environment variables should overwrite the defaults."""
    # Set the defaults.
    defaults = {
        "TEST_VAR": "defaults",
    }

    # Create the environment variable.
    monkeypatch.setenv("DJANGO_ENV_TEST_VAR", "environment")

    expected = {
        "TEST_VAR": "environment",
    }

    actual = DSL.load_secrets(**defaults)

    assert actual == expected


def test_load_secrets_environment_overwrites_files(fs, monkeypatch):
    """Environment variables should overwrite the files."""
    # Set the defaults.
    defaults = {}

    # Create the file.
    fn = ".env"
    fs.create_file(fn)
    with open(fn, "w") as file:
        file.write('TEST_VAR = "file"')

    # Create the environment variable.
    monkeypatch.setenv("DJANGO_ENV_TEST_VAR", "environment")

    expected = {
        "TEST_VAR": "environment",
    }

    actual = DSL.load_secrets(**defaults)

    assert actual == expected


def test_load_secrets_files_only_overwrite_defaults(fs):
    """Files should only overwrite available defaults."""
    # Set the defaults.
    defaults = {
        "TEST_VAR": "defaults",
    }

    # Create the file.
    fn = ".env"
    fs.create_file(fn)
    with open(fn, "w") as file:
        file.write(
            r"""TEST_VAR = "file"
TEST_VAR2 = "two"
"""
        )

    expected = {
        "TEST_VAR": "file",
    }

    actual = DSL.load_secrets(**defaults)

    assert actual == expected


def test_load_secrets_environment_only_overwrites_defaults(fs, monkeypatch):
    """Environment variables should only overwrite available defaults."""
    # Set the defaults.
    defaults = {
        "TEST_VAR": "defaults",
    }

    # Create the environment variable.
    monkeypatch.setenv("DJANGO_ENV_TEST_VAR", "environment")
    monkeypatch.setenv("DJANGO_ENV_TEST_VAR2", "environment2")

    expected = {
        "TEST_VAR": "environment",
    }

    actual = DSL.load_secrets(**defaults)

    assert actual == expected


def test_load_secrets_environment_files_only_overwrites_defaults(fs, monkeypatch):
    """New variables should only overwrite available defaults."""
    # Set the defaults.
    defaults = {
        "TEST_VAR": "test",
    }

    # Create the file.
    fn = ".env"
    fs.create_file(fn)
    with open(fn, "w") as file:
        file.write(
            r"""TEST_VAR = "file"
TEST_VAR2 = "file2"
"""
        )

    # Create the environment variable.
    monkeypatch.setenv("DJANGO_ENV_TEST_VAR", "environment")
    monkeypatch.setenv("DJANGO_ENV_TEST_VAR2", "environment2")

    expected = {
        "TEST_VAR": "environment",
    }

    actual = DSL.load_secrets(**defaults)

    assert actual == expected
