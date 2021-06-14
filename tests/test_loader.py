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

sys.path.insert(0, "/home/gray/src/work/django-loader")

import loader  # noqa: E402


def test_load_environment(monkeypatch):
    """Test load_environment() very simply."""
    monkeypatch.setenv("DJANGO_ENV_TEST_VAR", "test")
    expected = {
        "TEST_VAR": "test",
    }
    actual = loader.load_environment()

    assert actual == expected


def test_load_environment_missing():
    """Test load_environment() very simply."""
    expected = {}
    actual = loader.load_environment()

    assert actual == expected
