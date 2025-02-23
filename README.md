# code-review

![Code Review Checks](https://github.com/MaximTar/code-review/actions/workflows/code-review.yml/badge.svg)

### linters

```shell
flake8 linters_example.py
pylint linters_example.py
black [--diff] linters_example.py
```

### mypy

```shell
mypy mypy_example.py
```

### bandit

```shell
bandit bandit_example.py
```

### pre-commit

```shell
pre-commit run --all-files
```