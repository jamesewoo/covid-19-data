.PHONY: clean code_format install sync test

install: pyproject.toml
	poetry install

test: install
	poetry run pytest

code_format:
	poetry run isort covid_19_data tests
	poetry run flake8 .
	poetry run black .

sync:
	git fetch upstream
	git merge upstream/master

plot: install
	poetry run python -m covid_19_data.covid_utils

clean:
	rm -rf plots
