start:
	uv run flask --app src/app --debug run --port 8080

lint:
	ruff check

test:
	pytest -v