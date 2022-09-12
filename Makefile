ifeq ($(shell test -e '.env' && echo -n yes),yes)
	include .env
endif

# Manually define main variables

ifndef APP_PORT
override APP_PORT = 8000
endif

ifndef APP_HOST
override APP_HOST = 127.0.0.1
endif


IMAGE_NAME = template_application
TEST = poetry run python -m pytest --verbosity=2 --showlocals --log-level=DEBUG
CODE = app tests
ALEMBIC_PATH = app/db/migrator/alembic.ini

db:
	docker-compose up -d database

run:
	make db && uvicorn app.__main__:app --host ${APP_HOST} --port ${APP_HOST} --reload

test:
	make db && $(TEST)

docker-container:
	docker-compose up -d --build

migrate:
	alembic -c $(ALEMBIC_PATH) upgrade head

format:
	isort $(CODE)
	black -S -l 79 $(CODE)

lint:
	pylint $(CODE)
