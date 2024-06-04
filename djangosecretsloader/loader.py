# ******************************************************************************
#
# django-loader, a configuration and secret loader for Django
#
# Copyright 2021-2024 Jeremy A Gray <gray@flyquackswim.com>.
#
# SPDX-License-Identifier: MIT
#
# ******************************************************************************

"""Load Django settings.

Load Django settings from defaults, files, or the environment, in that
order.
"""

import json
import os
import sys
import warnings
from pathlib import Path

import bespon
import toml
from django.core.exceptions import ImproperlyConfigured
from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError

from .config import _create_argument_parser


def main(argv=None):
    """Provide the executable interface to django-loader.

    Parameters
    ----------
    argv : list, optional
        A list of arguments for the ``argparse`` parser.
    """
    args = _create_argument_parser().parse_args(argv)

    # Generate a Django SECRET_KEY.
    if args.generate_secret_key:
        print(generate_secret_key())
        sys.exit(0)
    # Validate the secrets.
    elif args.validate_secrets:
        try:
            # Validate the file format.
            if _validate_file_format(args.file):
                sys.exit(0)
        except ImproperlyConfigured as error:
            print(error)
            sys.exit(1)
    # FIXME:  load and dump environment
    else:
        print(
            dump_secrets(
                fmt=args.dump,
                **load_secrets(
                    fn=args.file,
                    prefix=args.prefix,
                ),
            )
        )


def generate_secret_key():
    """Generate a secret key for a Django app.

    Generate a secret key for a Django app, using
    ``django.core.management.utils.get_random_secret_key``.

    Returns
    -------
    string
        A random secret key.
    """
    from django.core.management.utils import get_random_secret_key

    return get_random_secret_key()


def load_secrets(
    fn=None,
    prefix="DJANGO_ENV_",
    **kwargs,
):
    """Load a list of configuration variables.

    Return a dictionary of configuration variables, as loaded from a
    configuration file or the environment.  Default key/value pairs
    may be passed as ``kwargs``.

    Parameters
    ----------
    fn : str, optional
        Configuration filename, defaults to ``.env`` if not defined in
        the environment as ``DJANGO_LOADER_ENV_FILE``.  May be in
        TOML, JSON, YAML, or BespON formats.  Formats will be
        attempted in this order.
    prefix : str, optional
        Prefix for environment variables.  This prefix will be
        prepended to all variable names before searching for them in
        the environment.
    **kwargs : dict, optional
        Dictionary with configuration variables as keys and default
        values as values.

    Returns
    -------
    dict
        A dictionary of configuration variables and their values.
    """
    if fn is None:
        fn = os.getenv("DJANGO_LOADER_ENV_FILE", ".env")

    return _merge(kwargs, _load_secrets_file(fn), _load_secrets_environment(prefix))


def dump_secrets(fmt="TOML", **kwargs):
    """Dump a secrets dictionary to the specified format.

    Dump a secrets dictionary to the specified format, defaulting to
    TOML.

    Parameters
    ----------
    fmt : str, optional
        The dump format, one of ``TOML``, ``JSON``, ``YAML``,
        ``BespON``, or ``ENV``.
    **kwargs : dict
        A dictionary of configuration variables.
    """
    if fmt == "TOML":
        return toml.dumps(kwargs)
    elif fmt == "JSON":
        return json.dumps(kwargs, indent=2)
    elif fmt == "YAML":
        # Let's jump through some hoops for the sake of streams.
        # https://yaml.readthedocs.io/en/latest/example.html#output-of-dump-as-a-string
        from ruamel.yaml.compat import StringIO

        stream = StringIO()
        yaml = YAML(typ="safe")
        yaml.dump(kwargs, stream)
        return stream.getvalue()
    elif fmt == "BespON":
        return bespon.dumps(kwargs)
    else:
        return _dump_secrets_environment(kwargs)


def _load_secrets_environment(prefix="DJANGO_ENV_"):
    """Load Django configuration variables from the enviroment.

    This function searches the environment for variables prepended
    with ``prefix``.  Currently, this function only reliably works for
    string variables, but hopefully will work for other types,
    dictionaries, and lists in the future.

    Parameters
    ----------
    prefix : str, optional
        Prefix for environment variables.  This prefix should be
        prepended to all valid variable names in the environment.

    Returns
    -------
    dict
        A dictionary, possibly empty, of configuration variables and
        values.
    """
    config = {}

    for key, value in os.environ.items():
        if key.startswith(prefix):
            # Find the prefixed values and strip the prefix.
            name = key.removeprefix(prefix)

            if "__" not in name:
                # Find the non-dict and non-list pairs and add them to
                # the dict.
                config[name] = value
            else:
                # Handle the flattened data structures, treating the
                # list type variables as dicts.
                # Based on:
                # https://gist.github.com/fmder/494aaa2dd6f8c428cede
                keys = name.split("__")
                sub_config = config
                for k in keys[:-1]:
                    try:
                        if not isinstance(sub_config[k], dict):
                            raise ImproperlyConfigured(
                                f"{k} is defined multiple times in the environment."
                            )
                        sub_config = sub_config[k]
                    except KeyError:
                        sub_config[k] = {}
                        sub_config = sub_config[k]
                sub_config[keys[-1]] = value

    config = _convert_listdict_to_list(config)

    return config


def _load_secrets_file(fn, raise_bad_format=True):
    """Attempt to load configuration variables from ``fn``.

    Attempt to load configuration variables from ``fn``.  If ``fn``
    does not exist or is not a recognized format, return an empty
    dict.  Raises ``ImproperlyConfigured`` if the file exists and does
    not match a recognized format unless ``raise_bad_format`` is
    ``False``.

    Parameters
    ----------
    fn : str
        Filename from which to load configuration values.
    raise_bad_format : bool, optional
        Determine whether to raise
        ``django.core.exceptions.ImproperlyConfigured`` if the file
        format is not recognized.  Default is ``True``.

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
        warnings.warn(f'File "{fn}" does not exist.')
        return secrets

    # Attempt to load TOML, since python.
    with open(fn, "r") as f:
        try:
            secrets = toml.load(f)
            return secrets
        except toml.TomlDecodeError:
            pass
    # Attempt to load JSON.
    with open(fn, "r") as f:
        try:
            secrets = json.load(f)
            return secrets
        except json.JSONDecodeError:
            pass
    # Attempt to load YAML, with ruamel.yaml and YAML 1.2.
    # Overachiever.
    with open(fn, "r") as f:
        try:
            yaml = YAML(typ="safe")
            secrets = yaml.load(f)
            return secrets
        except YAMLError:
            pass
    # Attempt to load BespON.  Geek.
    with open(fn, "r") as f:
        try:
            secrets = bespon.load(f)
            return secrets
        except bespon.erring.DecodingException:
            pass

    if raise_bad_format:
        raise ImproperlyConfigured(
            f"Configuration file {Path(fn).resolve()} is not a recognized format."
        )

    return secrets


def _dump_secrets_environment(config, prefix="DJANGO_ENV_", export=True):
    """Dump configuration as an environment variable string.

    Dump configuration as an environment variable string, hopefully
    compatible with Bourne shells.  Tested exclusively with bash.

    Parameters
    ----------
    config : dict
        The configuration dict.
    prefix : str, optional
        Prefix for environment variables.  This prefix should be
        prepended to all valid variable names in the environment.
    export : bool, optional
        Prepend each environment variable string with "export ", or
        not.

    Returns
    -------
    string
        The current configuration as a string setting environment
        variables.
    """
    stack = []
    dumps = []
    if export:
        exp = "export "
    else:
        exp = ""

    # Convert the config dict into a list (stack).
    for k, v in config.items():
        stack.append((k, v))

    while stack:
        (k, v) = stack.pop(0)
        if isinstance(v, list):
            for i, sv in enumerate(v):
                stack.append((f"{k}__{i}", sv))
        elif isinstance(v, dict):
            for sk, sv in v.items():
                stack.append((f"{k}__{sk}", sv))
        else:
            dumps.append(f"{str(k)}='{str(v)}'")

    return "\n".join(f"{exp}{prefix}{line}" for line in dumps)


def _merge(defaults, file, env):
    """Merge configuration from defaults, file, and environment.

    Parameters
    ----------
    defaults : dict
        Default configuration dictionary.
    file : dict
        File configuration dictionary.
    env : dict
        Environment configuration dictionary.

    Returns
    -------
    dict
        A dictionary of configuration variables and their values.
    """
    config = defaults

    if defaults:
        # Merge in file and environment options, if they exist in the
        # defaults.
        for k, v in file.items():
            if k in config:
                config[k] = v

        for k, v in env.items():
            if k in config:
                config[k] = v

        return config

    # Merge all file and environment options, with no defaults.
    for k, v in file.items():
        config[k] = v

    for k, v in env.items():
        config[k] = v

    return config


def _keys_are_indices(d):
    """Determine if the keys of a dict are list indices.

    Parameters
    ----------
    d : dict
        A dictionary that may only have list indices as keys.

    Returns
    -------
    bool
        ``True`` if all keys of a dict are list indices, ``False``
        otherwise.
    """
    # All integers?
    keys = []
    for k in d.keys():
        try:
            keys.append(int(k))
        except ValueError:
            return False

    keys = sorted(keys)

    # Zero start?
    if min(keys) != 0:
        return False

    # Consecutive?
    if keys != list(range(0, max(keys) + 1)):
        return False

    return True


def _convert_dict_to_list(d):
    """Convert a list-style dict to a list.

    Parameters
    ----------
    d : dict
        A dictionary with list indices as keys.

    Returns
    -------
    list
        The index-sorted values of the provided dictionary.
    """
    keys = sorted(d.keys())
    the_list = []
    for k in keys:
        the_list.append(d[k])

    return the_list


def _convert_listdict_to_list(d):
    """Convert lists as dicts to lists in a data structure.

    Convert lists as dicts to lists in a data structure that may
    contain lists of dicts or dicts of dicts, descending as necessary.

    Parameters
    ----------
    d : dict
        A dictionary, possibly containing other data structures.

    Returns
    -------
    list
        The index-sorted values of the provided dictionary.
    """
    for k, v in d.items():
        if isinstance(d[k], dict):
            # If the item points a dict, descend.
            d[k] = _convert_listdict_to_list(d[k])
            # We're back.  Now check if the dict is a list-style dict
            # and maybe convert to a list.
            if _keys_are_indices(d[k]):
                d[k] = _convert_dict_to_list(d[k])

    return d


def _validate_file_format(fn):
    """Validate format of ``fn``.

    Validate that the file ``fn`` is in one of the recognized formats.
    Return ``True`` if the format is valid and raises
    ``ImproperlyConfigured`` if the file does not exist or does not
    match a recognized format.

    Parameters
    ----------
    fn : str
        Filename from which to load configuration values.

    Returns
    -------
    bool
        Returns ``True`` if the file's format is valid.

    Raises
    ------
    django.core.exceptions.ImproperlyConfigured
        Raises an ``ImproperlyConfigured`` exception if the file does
        not exist or if the format is not recognized.
    """
    # Raise if the file does not exist.
    if not Path(fn).is_file():
        raise ImproperlyConfigured(f"Secrets file {Path(fn).resolve()} does not exist.")

    # TOML.
    with open(fn, "r") as f:
        try:
            toml.load(f)
            print(f"Secrets file {Path(fn).resolve()} recognized as TOML.")
            return True
        except toml.TomlDecodeError as error:
            print(f"toml error: {error}")
            print(f"Secrets file {Path(fn).resolve()} not recognized as TOML.")
            pass

    # JSON.
    with open(fn, "r") as f:
        try:
            json.load(f)
            print(f"Secrets file {Path(fn).resolve()} recognized as JSON.")
            return True
        except json.JSONDecodeError as error:
            print(f"json error: {error}")
            print(f"Secrets file {Path(fn).resolve()} not recognized as JSON.")
            pass

    # YAML.
    with open(fn, "r") as f:
        try:
            yaml = YAML(typ="safe")
            yaml.load(f)
            print(f"Secrets file {Path(fn).resolve()} recognized as YAML.")
            return True
        except YAMLError as error:
            print(f"yaml error: {error}")
            print(f"Secrets file {Path(fn).resolve()} not recognized as YAML.")
            pass

    # BespON.
    with open(fn, "r") as f:
        try:
            bespon.load(f)
            print(f"Secrets file {Path(fn).resolve()} recognized as BespON.")
            return True
        except bespon.erring.DecodingException as error:
            print(f"bespon error: {error}")
            print(f"Secrets file {Path(fn).resolve()} not recognized as BespON.")
            pass

    raise ImproperlyConfigured(
        f"Configuration file {Path(fn).resolve()} is not a recognized format."
    )

    return False
