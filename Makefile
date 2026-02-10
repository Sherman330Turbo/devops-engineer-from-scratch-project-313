start:
	uv run flask --app src/app --debug run --port 8080

install:
	pip install -e . ".[dev]"

lint:
	python3 -m ruff check .

test:
	python3 -m pytest