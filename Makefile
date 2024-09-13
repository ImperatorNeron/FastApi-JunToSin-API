DC = docker compose
DL = docker logs
EXEC = docker exec -it

APP_FILE = docker_compose/app.yaml
APP_CONTAINER = main-app

STORAGES_FILE = docker_compose/storages.yaml
STORAGES_CONTAINER = postgresql-container

ENV = --env-file .env

ALREV = alembic revision
ALUP = alembic upgrade
ALDOWN = alembic downgrade

.PHONY: storages
storages:
	${DC} -f ${STORAGES_FILE} ${ENV} up --build -d

.PHONY: storages-logs
storages-logs:
	${DL} ${STORAGES_CONTAINER} -f

.PHONY: storages-down
storages-down:
	${DC} -f ${STORAGES_FILE} ${ENV} down

.PHONY: app
app:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} ${ENV} up --build -d

.PHONY: app-logs
app-logs:
	${DL} ${APP_CONTAINER} -f

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} ${ENV} down

.PHONY: migrations
migrations:
	${EXEC} ${APP_CONTAINER} ${ALREV} -m "$(message)"

.PHONY: auto-migrations
auto-migrations:
	${EXEC} ${APP_CONTAINER} ${ALREV} --autogenerate -m "$(message)"

.PHONY: migrate-up
migrate-up:
	${EXEC} ${APP_CONTAINER} ${ALUP} head

.PHONY: migrate-down
migrate-down:
	${EXEC} ${APP_CONTAINER} ${ALDOWN} -1