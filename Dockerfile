FROM python:3.10.12-alpine

LABEL authors="sorxill"

EXPOSE 8000

WORKDIR /code

RUN pip install --upgrade pip
RUN apk add gcc musl-dev libffi-dev
RUN pip install poetry

COPY . /code

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --without test-dev

CMD ["poetry", "run", "uvicorn", "src.main:tracker", "--host", "0.0.0.0", "--port", "8000"]
