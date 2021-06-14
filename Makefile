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

.PHONY : build clean commit dist lint pip test test-all upload upload-test

test-all:
	pytest -vv --cov loader --cov-report term --cov-report html

build :
	# cd docs && make html
	pip install -q build
	python -m build

clean :
	# cd docs && make clean
	rm -rf build
	rm -rf dist
	rm -rf django_loader.egg-info

commit :
	pre-commit run --all-files

dist : clean build

lint :
	flake8 --exit-zero
	isort --check . || exit 0
	black --check .

pip :
	pip install -r requirements.txt

test:
	pytest

requirements.txt: poetry.lock
	./freeze.sh > $(@)

upload:
	python3 -m twine upload --verbose dist/*

upload-test:
	python3 -m twine upload --verbose --repository testpypi dist/*
