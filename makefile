# create .env files
init: env_local env/local/.env.celery env/local/.env.db env/local/.env.web

env_local:
	mkdir -p env/local

env/local/.env.celery: env/sample/.env.celery
	cp env/sample/.env.celery env/local/.env.celery

env/local/.env.db: env/sample/.env.db
	cp env/sample/.env.db env/local/.env.db

env/local/.env.web: env/sample/.env.web
	cp env/sample/.env.web env/local/.env.web

# docker-compose build / up
start:
	docker-compose -f docker-compose.local.yml up --build

detach:
	docker-compose -f docker-compose.local.yml up --build -d

stop:
	docker-compose -f docker-compose.local.yml down
