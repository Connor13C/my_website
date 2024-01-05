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
    Comments
)
from resources.auth import (
    UserRegister,
    User,
    UserLogin,
    UserLogout,
    TokenRefresh,
    OAuthServerLogin,
    OAuthServerAuthorize
)


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
    # @jwt.user_claims_loader
    # def add_claims_to_jwt(identity):
    #     if identity == 1:
    #         return {'is_admin': True}
    #     return {'is_admin': False}
    #
    # @jwt.token_in_blacklist_loader
    # def check_if_token_in_blacklist(decrypted_token):
    #     return decrypted_token['jti'] in BLACKLIST
    #
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
    api.add_resource(UserRegister, '/register')
    api.add_resource(User, '/user/<int:user_id>')
    api.add_resource(UserLogin, '/login')
    api.add_resource(TokenRefresh, '/refresh')
    api.add_resource(UserLogout, '/logout')

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
