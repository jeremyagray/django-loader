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


def test__process_defaults_odd_length():
    """Should raise ``ValueError``."""
    with pytest.raises(ValueError):
        DSL._process_defaults(["MY_VAR"])
