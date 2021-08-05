.PHONY: docs clean

docs:
	sphinx-build -M html "docs" "build"

clean:
	rm -rf build
	rm -rf dist
	rm README.rst

lint:
	pylint curvenote_template

format:
	isort curvenote_template
	black curvenote_template

build:
	m2r README.md --overwrite
	python -m build

deploy-test:
	python -m twine upload --repository-url=https://test.pypi.org/legacy/ dist/*

deploy:
	python -m twine upload dist/*