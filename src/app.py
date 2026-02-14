from flask import Flask
from sqlmodel import SQLModel

from .db import engine
from .errors import register_error_handlers
from .routes import register_routes


def create_app() -> Flask:
    app = Flask(__name__)

    SQLModel.metadata.create_all(engine)

    register_routes(app)
    register_error_handlers(app)

    return app
