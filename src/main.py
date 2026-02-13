import os

import sentry_sdk

from src.app import app

sentry_dns = os.environ.get("SENTRY_DNS", None)

if sentry_dns:
    sentry_sdk.init(
        dsn=sentry_dns,
    )

if __name__ == "__main__":
    app.run()
