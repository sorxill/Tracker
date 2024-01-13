FROM python:3.10.12-alpine

WORKDIR /app

RUN pip install --upgrade pip
RUN apk add gcc musl-dev libffi-dev
RUN pip install poetry

COPY . /app

EXPOSE 4000

RUN poetry install --without dev


CMD ["poetry", "run", "uvicorn", "--reload", "src.main:tracker", "--host=0.0.0.0", "--port=4000"]
