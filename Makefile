install: pyproject.toml
	poetry install

make test: install
	poetry run pytest

make code_format:
	poetry run isort covid_19_data tests
	poetry run flake8 .
	poetry run black .

make sync:
	git fetch upstream
	git rebase upstream/master
