.PHONY: list
list:
	@grep '^\w*:' Makefile

.PHONY: test
test:
	. ../venv/bin/activate; PYTHONPATH=tests:src python -m unittest discover -s tests

.PHONY: update
update:
	. ../venv/bin/activate; python -mpip install -U -e '.[devtools]'

.PHONY: lint
lint:
	. ../venv/bin/activate; ruff format .; ruff .; mypy .

.PHONY: docker-build
docker-build:
	docker build -t mood-of-the-day .

.PHONY: docker-start
docker-start:
	docker run --detach --expose 8000:8000 --name mood-of-the-day mood-of-the-day --daemon
