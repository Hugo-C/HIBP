qa:
  ruff check --no-fix
  ruff format --check --diff

fix-qa:
  ruff check --fix
  ruff format

test:
  pytest
