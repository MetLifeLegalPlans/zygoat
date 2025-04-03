all: clean deps
	poetry run zygoat last-run

clean:
	rm -rf last-run

deps: pyproject.toml
	poetry install
