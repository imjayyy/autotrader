DOCKER_BUILD_IMAGE_NAME = autotrader.az/app

install: docker-build docker-migrate-database docker-setup-superuser
run: docker-migrate-database docker-run-all


docker-build:
	docker build \
		--progress=plain \
		--target=app \
		-t $(DOCKER_BUILD_IMAGE_NAME) \
		.

docker-run-all:
	docker-compose up --remove-orphans

start-db:
	docker-compose up --remove-orphans --d db

docker-stop:
	docker-compose down

docker-stop-w-volumes:
	docker-compose down --volumes

docker-migrate-database:
	docker-compose run \
	--rm \
	django-server \
	python3 manage.py migrate

docker-setup-superuser:
	docker-compose run \
	--rm \
	django-server \
	python3 manage.py createsuperuser