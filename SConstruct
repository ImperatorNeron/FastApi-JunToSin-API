import os

DC = "docker compose"
DL = "docker logs"
EXEC = "docker exec -it"
APP_FILE = "docker_compose/app.yaml"
APP_CONTAINER = "main-app"
STORAGES_FILE = "docker_compose/storages.yaml"
TEST_STORAGES_FILE = "docker_compose/test_storages.yaml"
STORAGES_CONTAINER = "postgresql-container"
TEST_STORAGES_CONTAINER = "postgresql-test-container"
ENV = "--env-file .env.docker"
ALREV = "alembic revision"
ALUP = "alembic upgrade"
ALDOWN = "alembic downgrade"
TEST = "pytest --cache-clear"


def storages(target, source, env):
    command = f"{DC} -f {STORAGES_FILE} {ENV} up -d"
    return os.system(command)


def storages_logs(target, source, env):
    command = f"{DL} {STORAGES_CONTAINER} -f"
    return os.system(command)


def storages_down(target, source, env):
    command = f"{DC} -f {STORAGES_FILE} {ENV} down"
    return os.system(command)


def app(target, source, env):
    command = f"{DC} -f {APP_FILE} -f {STORAGES_FILE} -f {TEST_STORAGES_FILE} {ENV} up --build -d"
    return os.system(command)


def app_logs(target, source, env):
    command = f"{DL} {APP_CONTAINER} -f"
    return os.system(command)


def app_down(target, source, env):
    command = f"{DC} -f {APP_FILE} -f {STORAGES_FILE} -f {TEST_STORAGES_FILE} {ENV} down"
    return os.system(command)


def migrations(target, source, env):
    message = env.get("message", "default migration")
    command = f"{EXEC} {APP_CONTAINER} {ALREV} -m '{message}'"
    return os.system(command)


def auto_migrations(target, source, env):
    message = env.get("message", "default")
    command = f"{EXEC} {APP_CONTAINER} {ALREV} --autogenerate -m '{message}'"
    return os.system(command)


def migrate_up(target, source, env):
    command = f"{EXEC} {APP_CONTAINER} {ALUP} head"
    return os.system(command)


def migrate_down(target, source, env):
    command = f"{EXEC} {APP_CONTAINER} {ALDOWN} -1"
    return os.system(command)


def run_tests(target, source, env):
    command = f"{EXEC} {APP_CONTAINER} {TEST}"
    return os.system(command)


Command("storages", [], storages)
Command("storages-down", [], storages_down)
Command("storages-logs", [], storages_logs)
Command("up", [], app)
Command("down", [], app_down)
Command("logs", [], app_logs)
Command("migrations", [], migrations)
Command("auto-migrations", [], auto_migrations)
Command("migrate-up", [], migrate_up)
Command("migrate-down", [], migrate_down)
Command("migrate-down", [], migrate_down)
Command("run-tests", [], run_tests)
