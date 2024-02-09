# Tracker

**OPEN DOCKER DESKTOP(DAEMON)**
1. `docker-compose -f docker-compose-local.yaml up --build -d`
2. Now u have tables. U can test ur handlers.

- If u have problems like as: port 0.0.0.0:5432 is listen(bind) - u need in local terminal use command `sudo lsof -i :5432` / `sudo lsof -i :5433` . Ur next step is check the PID process running. After that run the command `sudo kill -9 <PID>`.

- For some problems write dev's.

### Test Database
1. New migrations - `alembic --name alembic_test revision -m "new rev for test" --autogenerate`
2. Add migrations on test database - `alembic --name alembic_test upgrade heads`
