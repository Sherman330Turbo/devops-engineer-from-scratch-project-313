FROM python:3.14.3-slim-bookworm

WORKDIR /app

COPY pyproject.toml /app/

RUN python3 -m pip install -e ".[dev]"

COPY /src ./src

EXPOSE 8080

CMD ["python3", "-m", "flask", "--app", "src/main.py", "run", "--host=0.0.0.0", "--port=8080"]