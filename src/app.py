from flask import Flask

app = Flask(__name__)


@app.route("/ping")
def get_ping():
    return "pong"


@app.route("/err")
def get_err():
    1 / 0
    return "pong"
