FROM node:23 AS builder

WORKDIR /build

COPY package*.json ./

RUN npm install --only=production

COPY . .

RUN npm run build

FROM python:3.12

ENV POETRY_VERSION=2.0.1

WORKDIR /code

COPY pyproject.toml poetry.lock /code/

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.in-project true --local && \
    poetry sync --only main --compile

COPY ./src /code/src

COPY --from=builder /build/src/static /code/src/static

RUN chown -R 1001:1001 /code

USER 1001

ENTRYPOINT ["poetry", "run"]

CMD ["fastapi", "run", "src/api/main.py", "--port", "80"]