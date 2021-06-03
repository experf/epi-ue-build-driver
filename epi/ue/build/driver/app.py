# save this as app.py
from flask import Flask

def make_app():
    app = Flask(__name__)

    @app.route("/")
    def hello():
        return "Hello, World!"

    return app
