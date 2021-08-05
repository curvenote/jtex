# Contributing to Curvenote Template

## Development

To get started create a virtual environment and install dev dependencies. This will also install the package as a local dependency ready for development.

```
  python -m venv env
  source env/bin/activate
  python -m pip install -r requirements_dev.txt
```

Linting rules are included in the repo and you should run `black` before pushing changes to a PR.

```
  black curvenote_template
```

## Running the tests

Run the tests with `pytest` or `pytest-watch`
