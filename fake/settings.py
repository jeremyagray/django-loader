# ******************************************************************************
#
# django-loader, a configuration and secret loader for Django
#
# Copyright 2021-2024 Jeremy A Gray <gray@flyquackswim.com>.
#
# SPDX-License-Identifier: MIT
#
# ******************************************************************************

"""Fake project settings."""

import djangosecretsloader as DSL

secrets = DSL.load_secrets(
    **{
        "ALLOWED_HOSTS": [],
        "SECRET_KEY": "",
        "DEBUG": True,
        "DB": {},
    }
)

ALLOWED_HOSTS = secrets["ALLOWED_HOSTS"]
SECRET_KEY = secrets["SECRET_KEY"]
DEBUG = secrets["DEBUG"]

ROOT_URLCONF = "fake.urls"

DATABASES = {
    "default": secrets["DB"],
}
