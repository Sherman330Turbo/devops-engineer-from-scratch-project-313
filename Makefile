FRAMEWORK ?= react
API_URL ?= http://127.0.0.1:8080
DOCKER_TAG ?= sherman330turbo/pyp-example

.PHONY: start start-backend start-frontend build-docker install install-back install-front lint test

start:
	npx concurrently \
		--kill-others-on-fail \
		--names "back,front" \
		--prefix-colors "magenta,cyan" \
		"$(MAKE) start-backend" \
		"$(MAKE) start-frontend FRAMEWORK=$(FRAMEWORK)"

start-backend:
	uv run flask --app src/main --debug run --port 8080

start-frontend:
	@if [ "$(FRAMEWORK)" = "react" ]; then \
		API_URL="$(API_URL)" npx start-hexlet-devops-deploy-crud-frontend; \
	else \
		echo "No framework this time"; \
		exit 0; \
	fi

build-docker:
	docker build --no-cache -t "$(DOCKER_TAG)" .

install:install-back install-front

install-back:
	python3 -m pip install -e ".[dev]"

install-front:
	npm ci

lint:
	python3 -m ruff check .

test:
	python3 -m pytest