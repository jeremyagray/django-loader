#!/usr/bin/env python
#
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
"""django-loader script interface."""

import sys

sys.path.insert(0, "/home/gray/src/work/django-loader")

from loader import main  # noqa: E402

if __name__ == "__main__":
    main()
