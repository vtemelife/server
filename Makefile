clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + > /dev/null 2>&1
	find . -type f -name "*.pyc" -exec rm -rf {} + > /dev/null 2>&1

celery:
	celery -A config worker -l INFO --purge

celerybeat:
	celery -A config beat -l INFO

start:
	python manage.py collectstatic --noinput
	python manage.py migrate --noinput
	python manage.py runserver 0.0.0.0:8000

lint:
	flake8 --show-source apps

test:
	flake8 --show-source apps
	isort --check-only -rc apps --diff
	python manage.py makemigrations --dry-run --check
	pytest --ds=config.settings.test --cov=apps --cov-report=term --cov-report=html

all: clean lint

fix:
	black apps
	isort -rc apps

locale:
	python manage.py makemessages -l ru --ignore env

install:
	pip install -r requirements/dev.txt
	pre-commit install
