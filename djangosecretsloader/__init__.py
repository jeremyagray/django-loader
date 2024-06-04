# ******************************************************************************
#
# django-loader, a configuration and secret loader for Django
#
# Copyright 2021-2024 Jeremy A Gray <gray@flyquackswim.com>.
#
# SPDX-License-Identifier: MIT
#
# ******************************************************************************

"""django-loader module interface."""

from .config import _create_argument_parser
from .loader import _convert_dict_to_list
from .loader import _convert_listdict_to_list
from .loader import _dump_secrets_environment
from .loader import _keys_are_indices
from .loader import _load_secrets_environment
from .loader import _load_secrets_file
from .loader import _merge
from .loader import _validate_file_format
from .loader import dump_secrets
from .loader import generate_secret_key
from .loader import load_secrets
from .loader import main
