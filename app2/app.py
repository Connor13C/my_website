import os
from flask import Flask, jsonify
from flask_restful import Api
from flask import Flask
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError
from werkzeug.middleware.proxy_fix import ProxyFix
from celery import Celery

from db import db
from ma import ma
from oa import oauth
from app2.resources.endpoints import (
    Example,
    Projects,
    Project,
    Comments)
from resources.auth import OAuthServerLogin, OAuthServerAuthorize


def create_app():
    """Configures and creates Flask application. Includes ProxyFix expecting this to be inside a
    reverse proxy setup."""
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)
    app.config.from_object("config")
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    # app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
    api = Api(app)
    # jwt = JWTManager(app)

    @app.errorhandler(ValidationError)
    def handle_marshmallow_validation(err):
        return jsonify(err.messages), 400

    @app.before_first_request
    def create_tables():
        db.create_all()

    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    # @jwt.user_claims_loader
    # def add_claims_to_access_token(user):
    #     return user.roles
    #
    # @jwt.user_identity_loader
    # def user_identity_lookup(user):
    #     return {'name': user.name, 'email': user.email, 'ip': user.ip}

    api.add_resource(Example, '/', endpoint='homepage')
    api.add_resource(Projects, '/projects', endpoint='projects')
    api.add_resource(Project, '/projects/<project_id>', endpoint='projects.id')
    api.add_resource(Comments, '/projects/<project_id>/comments', endpoint='projects.comments')

    db.init_app(app)
    ma.init_app(app)
    oauth.init_app(app)
    return app


def create_celery():
    """Configures and creates celery application to run background tasks with the same abilities as the flask
    application but allows asynchronous tasks to be run during in background."""
    app = create_app()
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


if __name__ == "__main__":
    create_app().run(port=5000)
