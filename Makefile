all: clean deps
	poetry run zygoat test
	mv test last-run

clean:
	rm -rf last-run test

deps: pyproject.toml
	poetry install
