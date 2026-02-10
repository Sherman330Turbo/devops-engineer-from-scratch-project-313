start:
	uv run flask --app src/app --debug run --port 8080

lint:
	uv run ruff check

test:
	uv run pytest -v