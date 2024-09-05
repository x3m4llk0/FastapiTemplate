DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env
APP_FILE = docker-compose.yml
SERVICE = templateservice
APP_CONTAINER = $(SERVICE)-app
COMPOSE_FILES = docker-compose.yml


.PHONY: app
app:
	${DC} -f ${APP_FILE} -f ${COMPOSE_FILES} ${ENV} up --build -d

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

.PHONY: migrations
migrations:
	alembic revision --autogenerate -m "Added required tables"

.PHONY: migrate
migrate:
	alembic upgrade head

