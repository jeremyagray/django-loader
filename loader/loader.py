# ******************************************************************************
#
# django-loader, a configuration and secret loader for Django
#
# loader.py:  main loader functions
#
# Copyright (C) 2021 Jeremy A Gray <gray@flyquackswim.com>.
#
# SPDX-License-Identifier: MIT
#
# ******************************************************************************
#
"""Load Django settings.

Load Django settings from defaults, files, or the environment, in that
order.
"""

import json
import os
import sys
import types
from pathlib import Path

import bespon
import toml
from django.core.exceptions import ImproperlyConfigured
from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError


def load_secrets(fn=".env", prefix="DJANGO_ENV_", **kwargs):
    """Load a list of configuration variables.

    Return a dictionary of configuration variables, as loaded from a
    configuration file or the environment.  Values passed in as
    ``args`` or as the value in ``kwargs`` will be used as the
    configuration variable's default value if one is not found in the
    configuration file or environment.

    Parameters
    ----------
    fn : string, default=".env"
        Configuration filename, defaults to ``.env``.  May be in TOML,
        JSON, YAML, or BespOn formats.  Formats will be attempted in this
        order.
    prefix : string, default="DJANGO_ENV_"
        Prefix for environment variables.  This prefix will be
        prepended to all variable names before searching for them in
        the environment.
    kwargs : dict, optional
        Dictionary with configuration variables as keys and default
        values as values.

    Returns
    -------
    dict
        A dictionary of configuration variables and their values.

    Raises
    ------
    FileNotFoundError
        Raised if the configuration file is not found.
    django.core.exceptions.ImproperlyConfigured
        Raised if the the configuration file format is not recognized.
    """
    return merge(kwargs, load_file(fn), load_environment(prefix))


def merge(defaults, file, env):
    """Merge configuration from defaults, file, and environment."""
    config = defaults

    # Merge in file options, if they exist in the defaults.
    for (k, v) in file.items():
        if k in config:
            config[k] = v

    # Merge in environment options, if they exist in the defaults.
    for (k, v) in env.items():
        if k in config:
            config[k] = v

    return config


def load_file(fn, raise_bad_format=False):
    """Attempt to load configuration variables from ``fn``.

    Attempt to load configuration variables from ``fn``.  If ``fn``
    does not exist or is not a recognized format, return an empty dict
    unless ``raise_bad_format`` is ``True``.

    Parameters
    ----------
    fn : string
        Filename from which to load configuration values.
    raise_bad_format : boolean, default=False
        Determine whether to raise
        ``django.core.exceptions.ImproperlyConfigured`` if the file
        format is not recognized.  Default is ``False``.

    Returns
    -------
    dict
        A dictionary, possibly empty, of configuration variables and
        values.

    Raises
    ------
    django.core.exceptions.ImproperlyConfigured
        Raises an ``ImproperlyConfigured`` exception if the file
        format is not recognized and ``raise_bad_format`` is ``True``.
    """
    # Determine if the file actually exists, and bail if not.
    secrets = {}
    if not Path(fn).is_file():
        return secrets

    # Attempt to load TOML, since python.
    with open(fn, "r") as f:
        try:
            secrets = toml.load(f)
        except (toml.TomlDecodeError):
            pass
    # Attempt to load JSON.
    with open(fn, "r") as f:
        try:
            secrets = json.load(f)
        except (json.JSONDecodeError):
            pass
    # Attempt to load YAML, with ruamel.yaml and YAML 1.2.
    # Overachiever.
    with open(fn, "r") as f:
        try:
            yaml = YAML(typ="safe")
            secrets = yaml.load(f)
        except (YAMLError):
            pass
    # Attempt to load BespON.  Geek.
    with open(fn, "r") as f:
        try:
            secrets = bespon.load(f)
        except (bespon.erring.DecodingException):
            # Everything failed, so raise.
            if raise_bad_format:
                raise ImproperlyConfigured(
                    f"Configuration file {fn} is not a recognized format."
                )

    return secrets


def load_environment(prefix="DJANGO_ENV_", **kwargs):
    """Load Django configuration variables from the enviroment.

    This function searches the environment for variables prepended
    with ``prefix`` and attempts to validate that value against the
    list of values in ``validation`` or by calling the function stored
    in ``validation`` with the single argument of the value of the
    environment variable.

    Parameters
    ----------
    name : string, default="DJANGO_ENV_"
        The name of the variable to be loaded.  This name will be
        prefixed with ``prefix`` before searching the environment.
    validation : object
        Either a list of allowed values (defaults to the empty list)
        or a function accepting one parameter that validates the value
        and either returns the validated value or raises an
        ``ImproperlyConfigured`` exception.

    Returns
    -------
    string
        The value stored in the environment variable.

    Raises
    ------
    django.core.exceptions.ImproperlyConfigured
        Raises an ``ImproperlyConfigured`` exception on blank or
        non-existent values, with an error message.
    """
    config = {}
    for (k, v) in kwargs.items():
        var = prefix + k
        try:
            config[k] = os.environ[var]
        except KeyError:
            config[k] = kwargs[k]

    return config


def validate_not_empty_string(name, val):
    """Validate that ``val`` is not an empty string.

    Validate that ``val`` is not an empty string.

    Parameters
    ----------
    val : any
        Configuration variable to validate.

    Returns
    -------
    boolean
        ``True`` if ``val`` is not an empty string.

    Raises
    ------
    django.core.exceptions.ImproperlyConfigured
        Raises an ``ImproperlyConfigured`` exception on empty strings,
        with an error message.
    """
    if val == "":
        raise ImproperlyConfigured(f"{name} is an empty string and should not be")

    return True


def validate_falsy(name, val):
    """Validate that ``val`` is falsy.

    Validate that ``val`` is falsy according to
    https://docs.python.org/3/library/stdtypes.html#truth-value-testing.

    Parameters
    ----------
    val : any
        Configuration variable to validate.

    Returns
    -------
    boolean
        ``True`` if ``val`` is falsy.

    Raises
    ------
    django.core.exceptions.ImproperlyConfigured
        Raises an ``ImproperlyConfigured`` exception on truthy values,
        with an error message.
    """
    if val:
        raise ImproperlyConfigured(
            f"{name} has value {val} which is truthy, but should be falsy"
        )

    return True


def validate_truthy(name, val):
    """Validate that ``val`` is truthy.

    Validate that ``val`` is truthy according to
    https://docs.python.org/3/library/stdtypes.html#truth-value-testing.

    Parameters
    ----------
    val : any
        Configuration variable to validate.

    Returns
    -------
    boolean
        ``True`` if ``val`` is truthy.

    Raises
    ------
    django.core.exceptions.ImproperlyConfigured
        Raises an ``ImproperlyConfigured`` exception on falsy values,
        with an error message.
    """
    if not val:
        raise ImproperlyConfigured(
            f"{name} has value {val} which is falsy, but should be truthy"
        )

    return True


def set_or_fail_on_unset(val):
    """Raise ``ImproperlyConfigured()`` if ``val`` is not set.

    Return the configuration value if set, otherwise raise
    ``django.core.exceptions.ImproperlyConfigured()`` to abort.

    Parameters
    ----------
    val : string
        Configuration variable that should be set to a value.

    Returns
    -------
    string
        The variable value, if set.
    """
    if not val:
        raise ImproperlyConfigured("A required configuration variable is not set.")

    return val


def _validate(name, val, validation=[]):
    """Validate a django configuration variable."""
    env_name = "DJANGO_" + name

    if isinstance(validation, types.FunctionType):
        try:
            return validation(val)
        except ImproperlyConfigured:
            raise
    else:
        if len(validation) > 0:
            if not (val in validation):
                raise ImproperlyConfigured(
                    f"{name} can not have value {val};"
                    f" must be one of [{', '.join(validation)}]."
                )
                return

        print(f"{name} loaded from {env_name}.")
        return val


def dump_secrets(fmt="TOML", **kwargs):
    """Dump a secrets dictionary to the specified format.

    Dump a secrets dictionary to the specified format, defaulting to
    TOML.

    Parameters
    ----------
    fmt : string, default="TOML"
        The dump format, one of "TOML", "JSON", "YAML", "BespON", or
        "ENV" (not currently implemented).
    kwargs : dict
        A dictionary of configuration variables.

    Raises
    ------
    NotImplementedError
        Raises ``NotImplementedError`` for format ``ENV`` to dump
        environment variables.
    """
    if fmt == "TOML":
        print(toml.dumps(kwargs))
    elif fmt == "JSON":
        print(json.dumps(kwargs))
    elif fmt == "YAML":
        yaml = YAML(typ="safe")
        print(yaml.dump(kwargs, sys.stdout))
    elif fmt == "BespON":
        print(bespon.dumps(kwargs))
    elif fmt == "ENV":
        # print(env_dumps(kwargs))
        raise NotImplementedError

    return


def main():
    """Run as script, to access ``dump()`` functions."""
    dump_secrets(**load_secrets(**{"ALLOWED_HOSTS": ["bob is your uncle"]}))


if __name__ == "__main__":
    main()
