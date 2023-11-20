# ******************************************************************************
#
# django-loader, a configuration and secret loader for Django
#
# Copyright 2021-2023 Jeremy A Gray <gray@flyquackswim.com>.
#
# SPDX-License-Identifier: MIT
#
# ******************************************************************************
#
"""Integration tests."""

from django.conf import settings


def test_load_secrets():
    """Should load ``ALLOWED_HOSTS``."""
    actual = settings.ALLOWED_HOSTS
    expected = [
        "127.0.0.1",
        "192.168.1.67",
        "192.168.1.78",
        "localhost",
        "vulcan",
        "testserver",
    ]

    assert actual == expected
