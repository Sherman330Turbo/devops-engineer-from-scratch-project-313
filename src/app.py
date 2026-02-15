import os

from flask import Flask
from flask_cors import CORS
from sqlmodel import SQLModel

from .db import engine
from .errors import register_error_handlers
from .routes import register_routes


def create_app() -> Flask:
    app = Flask(__name__)

    if os.getenv("IS_DEVELOPMENT", "False") == "True":
        CORS(
            app,
            resources={
                r"/api/*": {
                    "origins": [
                        "http://127.0.0.1:5173",
                    ]
                }
            },
            supports_credentials=True,
            methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            expose_headers=["Content-Range"],
        )

    SQLModel.metadata.create_all(engine)

    register_routes(app)
    register_error_handlers(app)

    return app
