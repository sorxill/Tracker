# Tracker

**OPEN DOCKER DESKTOP**
1. `docker-compose -f docker-compose-local.yaml up`
2. Now u don't have migrations on your database. At so u need to go Docker Desktop. Open the title named exec and start command `poetry run alembic upgrade head`.
3. Now u have tables. U can test ur handlers.

If u have problems like as: port 0.0.0.0:5432 is listen(bind) - u need in local terminal use command `sudo lsof -i :5432`. Ur next step is check the PID proccess running. After that run the command `sudo kill -9 <PID>`.

For some problems write me.
