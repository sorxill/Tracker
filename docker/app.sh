#!/bin/busybox

poetry run alembic upgrade head

poetry run uvicorn --reload src.main:tracker --host=0.0.0.0 --port=4000