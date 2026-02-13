start:
	uv run flask --app src/main --debug run --port 8080

install:
	python3 -m pip install -e ".[dev]"

lint:
	python3 -m ruff check .

test:
	python3 -m pytest