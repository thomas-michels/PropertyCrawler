include ./.env

build:
	docker build -t property_services --no-cache .

run:
	docker run --env-file .env --name property_services -d --network=propertycrawler_crawler_network property_services
