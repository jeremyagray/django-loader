# ******************************************************************************
#
# django-loader, a configuration and secret loader for Django
#
# Makefile - chore makefile for django-blog
#
# Copyright (C) 2021 Jeremy A Gray <gray@flyquackswim.com>.
#
# SPDX-License-Identifier: MIT
#
# ******************************************************************************

python-modules = fake loader tests
python-files =

.PHONY : test-all
test-all:
	pytest -vv --cov fake --cov loader --cov-report term --cov-report html

.PHONY : build
build : docs
	pip install -q build
	python -m build

.PHONY : clean
clean :
	cd docs && make clean
	rm -rf build
	rm -rf dist
	rm -rf django_loader.egg-info

.PHONY : commit
commit :
	pre-commit run --all-files

.PHONY : dist
dist : clean build

.PHONY : docs
docs :
	cd docs && make html

.PHONY : lint
lint :
	flake8 --exit-zero $(python-modules) $(python-files)
	isort --check $(python-modules) $(python-files) || exit 0
	black --check $(python-modules) $(python-files)

.PHONY : lint-fix
lint-fix :
	isort $(python-modules) $(python-files)
	black $(python-modules) $(python-files)

.PHONY : pip
pip :
	pip install -r requirements.txt

.PHONY : test
test:
	pytest

.PHONY : upload
upload:
	python3 -m twine upload --verbose dist/*

.PHONY : upload-test
upload-test:
	python3 -m twine upload --verbose --repository testpypi dist/*

requirements.txt: poetry.lock
	./freeze.sh > $(@)
