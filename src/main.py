import os

import sentry_sdk
from dotenv import load_dotenv

from .app import create_app


def init_sentry():
    sentry_dsn = os.environ.get("SENTRY_DSN", None)
    if sentry_dsn:
        sentry_sdk.init(
            dsn=sentry_dsn,
        )


load_dotenv()
init_sentry()
app = create_app()
