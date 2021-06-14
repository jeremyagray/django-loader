#!/bin/bash
#
# ******************************************************************************
#
# django-loader, a configuration and secret loader for Django
#
# Copyright (C) 2021 Jeremy A Gray <gray@flyquackswim.com>.
#
# SPDX-License-Identifier: MIT
#
# ******************************************************************************

pip='/home/gray/.virtualenvs/django-loader/bin/pip'
sed='/usr/bin/sed'

${pip} freeze | ${sed} 's/ @ .*-\(.*\)\(-py[23]\|-cp39-cp39\|-cp36\|\.tar\).*$/==\1/' | ${sed} 's/^django-\(blog\|products\) .*$/git+file:\/\/\/home\/gray\/src\/git\/django-\1.git/'
