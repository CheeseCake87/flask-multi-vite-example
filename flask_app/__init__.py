from flask import Flask

from flask_app.extensions import imp


def create_app():
    app = Flask(__name__)
    imp.init_app(app)
    imp.import_app_resources()
    imp.import_blueprint("backend")
    imp.import_blueprint("frontend")

    return app
