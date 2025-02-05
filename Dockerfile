FROM python:3.12

ENV POETRY_VERSION=2.0.1

WORKDIR /code

COPY pyproject.toml poetry.lock /code/

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.in-project true --local && \
    poetry sync --only main --compile

COPY ./src /code/src

RUN chown -R 1001:1001 /code

USER 1001

ENTRYPOINT ["poetry", "run"]

CMD ["fastapi", "run", "src/api/main.py", "--port", "80"]