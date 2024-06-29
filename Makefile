.PHONY: docker-build
docker-build:
	docker build -t mood-of-the-day .

.PHONY: docker-start
docker-start:
	docker run --detach --expose 8000:8000 --name mood-of-the-day mood-of-the-day --daemon
