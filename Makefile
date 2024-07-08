DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env
APP_FILE = docker-compose.yml
APP_CONTAINER = servicename-app
SETUPDB = app/database/postgres/setupdb.py

.PHONY: app
app:
	${DC} -f ${APP_FILE} ${ENV} up --build -d

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} down

.PHONY: app-shell
app-shell:
	${EXEC} ${APP_CONTAINER} bash

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: test
test:
	${EXEC} ${APP_CONTAINER} pytest

.PHONY: db-drop
db-drop:
	${EXEC} ${APP_CONTAINER} python ${SETUPDB} drop

.PHONY: db-create
db-create:
	${EXEC} ${APP_CONTAINER} python ${SETUPDB} create

.PHONY: db-prepare
db-prepare:
	${EXEC} ${APP_CONTAINER} python ${SETUPDB} prepare

.PHONY: db-setup
db-setup:
	${EXEC} ${APP_CONTAINER} python ${SETUPDB} setup

.PHONY: db-alembic
db-alembic:
	${EXEC} ${APP_CONTAINER} python ${SETUPDB} alembic
