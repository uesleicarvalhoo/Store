# Variables
-include .env
PYTHONPATH = $(shell pwd)

run:
	@uvicorn "src.app:app" --port 5000 --reload

deploy: upgrade
	@poetry run gunicorn src.app:app -c "./src/gunicorn.py"

test:
	@ENVIRONMENT=test pytest tests

docker:
	@docker rm -f store || true
	@docker build -t store .
	@docker run --expose 80 --env-file .env.docker --name=store --network=global-default -p 8000:80 -d store make deploy

format:
	@black src tests migration
	@isort src tests migration
	@flake8 src tests migration
	@autoflake8 --remove-unused-variables --recursive --exclude=__init__.py --in-place src tests migration

revision:
	@PYTHONPATH="${PYTHONPATH}" poetry run alembic revision --autogenerate

upgrade:
	@PYTHONPATH="${PYTHONPATH}" poetry run alembic upgrade head

downgrade:
	@PYTHONPATH="${PYTHONPATH}" poetry run alembic downgrade head

clean-pyc:
	@find . -name "__pycache__" -exec rm -rf {} +
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
