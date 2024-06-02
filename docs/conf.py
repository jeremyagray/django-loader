# ******************************************************************************
#
# django-loader, a configuration and secret loader for Django
#
# Copyright 2021-2024 Jeremy A Gray <gray@flyquackswim.com>.
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
copyright = "2021-2024, Jeremy A Gray"
author = "Jeremy A Gray"
release = "0.0.12"

extensions = [
    "numpydoc",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
]

autosummary_generate = True

# All paths relative to this directory.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "alabaster"
