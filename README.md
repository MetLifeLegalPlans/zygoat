# zygoat

<img src="https://user-images.githubusercontent.com/640862/75250233-e287ea80-57a5-11ea-9d9f-553662a17706.jpeg" />

## What is zygoat?

`zygoat` is a command line tool used to bootstrap and configure a React/Django/Postgres stack web application.

Linting, test configuration, boilerplate, and development environment are automatically taken care of using `zygoat` so that you can get up and running faster.

`zygoat` also includes a preset deployment configuration to allow you to deploy your stack to an AWS environment with a single command. You'll get a full serverless AWS stack to keep things inexpensive and nimble.

## How do I use it?

Make a new git repository somewhere, we'll call it test-zg

```bash
mkdir test-zg && cd test-zg
git init
```

Install the zygoat package locally

```bash
pip install --user --upgrade ~/Projects/zygoat  # Or wherever you have it
```

If you're using the asdf version manager, reshim

```bash
asdf reshim python
```

Run zg commands, see if they fail

```bash
zg new test
zg update
zg delete
```

---

## Contributing

`zygoat` is developed using the [Poetry](https://python-poetry.org/docs/) packaging framework for Python projects to make development as simple and portable as possible.
