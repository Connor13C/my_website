import os
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from werkzeug.middleware.proxy_fix import ProxyFix
from celery import Celery

from db import db
from models.auth import JwtBlocklist
from resources.auth import (
    UserRegister,
    User,
    UserLogin,
    UserLogout
)
from resources.index import Index
from resources.client import Client, Clients
from resources.request import Request, RequestID, RequestList


def create_app():
    """Configures and creates Flask application. Includes ProxyFix expecting this to be inside a
    reverse proxy setup."""
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)
    app.config.from_object("config")
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    api = Api(app)
    api.add_resource(Index, '/')
    api.add_resource(UserRegister, '/register')
    api.add_resource(User, '/user/<int:user_id>')
    api.add_resource(UserLogin, '/login')
    api.add_resource(UserLogout, '/logout')
    api.add_resource(Client, '/client/<string:name>')
    api.add_resource(Clients, '/clients')
    api.add_resource(Request, '/request')
    api.add_resource(RequestID, '/request/<int:request_id>')
    api.add_resource(RequestList, '/requests')

    jwt = JWTManager(app)

    # @jwt.user_claims_loader
    # def add_claims_to_access_token(user):
    #     return user.roles

    # @jwt.user_identity_loader
    # def user_identity_lookup(user):
    #     return {'name': user.name, 'email': user.email, 'ip': user.ip}

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, jwt_payload: dict):
        """Callback function to check if a JWT exists in the database blocklist"""
        return JwtBlocklist.find_by_id(_id=jwt_payload['jti']) is not None

    # @jwt.expired_token_loader
    # def expired_token_callback():
    #     return jsonify({'description': 'The token has expired.', 'error': 'token_expired'}), 401
    #
    # @jwt.invalid_token_loader
    # def invalid_token_callback(error):
    #     return jsonify({'description': 'Signature verification failed.', 'error': 'invalid_token'}), 401
    #
    # @jwt.unauthorized_loader
    # def missing_token_callback(error):
    #     return jsonify({'description': 'Request does not contain an access token.', 'error': 'authorization_required'}), 401
    #
    # @jwt.needs_fresh_token_loader
    # def token_not_fresh_callback():
    #     return jsonify({'description': 'The token is not fresh.', 'error': 'fresh_token_required'}), 401
    #
    # @jwt.revoked_token_loader
    # def revoked_token_callback():
    #     return jsonify({'description': 'The token has been revoked.', 'error': 'token_revoked'}), 401

    db.init_app(app)
    with app.app_context():
        db.create_all()

    return app


def create_celery():
    """Configures and creates celery application to run background tasks with the same abilities as the flask
    application but allows asynchronous tasks to be run during in background."""
    app = create_app()
    celery = Celery(
        app.import_name,
        backend=app.config['RESULT_BACKEND'],
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
    create_app().run(host="0.0.0.0", port=5000, debug=True)
