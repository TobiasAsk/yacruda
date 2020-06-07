from flask import Flask
from flask_cors import CORS

from app.blueprint import Books
from app.model import init_app


def create_app(config=None) -> Flask:
    app = Flask(__name__)
    CORS(app)

    if config:
        app.config.from_mapping(config)
    else:
        app.config.from_pyfile('config.py', silent=False)

    app.register_blueprint(Books())
    init_app(app)

    return app
