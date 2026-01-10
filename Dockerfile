FROM python:3.12
WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN python -m pip install --upgrade pip \
    && pip install poetry \
    && poetry install --no-root \
    && poetry install --no-root

COPY app /app/app
ENTRYPOINT ["poetry", "run"]
CMD ["python", "-m", "app.main"]