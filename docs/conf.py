# ******************************************************************************
#
# django-loader, a configuration and secret loader for Django
#
# Copyright (C) 2021-2022 Jeremy A Gray <gray@flyquackswim.com>.
#
# SPDX-License-Identifier: MIT
#
# ******************************************************************************
#
"""Sphinx documentation configuration."""

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = "django-loader"
copyright = "2021-2022, Jeremy A Gray"
author = "Jeremy A Gray"
release = "0.0.10"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
]

autosummary_generate = True

# All paths relative to this directory.
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
html_static_path = ["_static"]

html_theme = "alabaster"
