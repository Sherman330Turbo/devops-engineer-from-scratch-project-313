from flask import Flask

app = Flask(__name__)

@app.route("/ping")
def get_ping():
    return "pong"