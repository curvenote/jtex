.PHONY: docs clean

docs:
	sphinx-build -M html "docs" "build"

clean:
	rm -rf build
	rm -rf dist

lint:
	pylint curvenote_template

format:
	isort curvenote_template
	black curvenote_template

build:
	python -m build

deploy:
	python -m twine upload dist/*