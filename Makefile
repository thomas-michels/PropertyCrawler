include ./.env

build:
	docker build -t property_services --no-cache .

run:
	docker run --env-file .env --name property_services -d --network=${NETWORK} property_services

migrate:
	alembic upgrade head
