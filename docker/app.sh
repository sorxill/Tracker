#!/bin/busybox

poetry run alembic upgrade head

poetry run alembic --name alembic_test upgrade heads

poetry run uvicorn --reload src.main:tracker --host=0.0.0.0 --port=4000