qa:
  ruff check --no-fix
  ruff format --check --diff

fix-qa:
  ruff check --fix
  ruff format

test:
  poetry run pytest

load_test:
  cd tests/load_test && locust