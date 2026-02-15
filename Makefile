FRAMEWORK ?= react
API_URL ?= http://127.0.0.1:8080

.PHONY: start start-backend start-frontend install lint test

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

install:
	python3 -m pip install -e ".[dev]"

lint:
	python3 -m ruff check .

test:
	python3 -m pytest