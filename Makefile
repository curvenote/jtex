.PHONY: docs clean

docs:
	sphinx-build -M html "docs" "build"

clean:
	rm -rf build
	rm -rf dist

lint:
	pylint jtex

format:
	isort jtex
	black jtex

build:
	python -m build

test:
	pytest

deploy-check:
	python -m twine check dist/*

deploy-test:
	python -m twine upload --repository-url=https://test.pypi.org/legacy/ dist/*

deploy: deploy-check
	python -m twine upload dist/*
