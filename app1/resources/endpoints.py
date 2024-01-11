import json

import flask_restful
from flask import Response, request
from flask_restful import Resource, reqparse
from resources.auth import introspect_token
from models.db import ProjectModel, CommentModel
from functools import wraps


def check_bearer_token(fn):
    """
    Decorator function that checks for valid bearer token. Missing and invalid tokens
    sends 401 Unauthorized response before the Resource this decorator is on is
    executed.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("authorization")
        if not auth_header or len(auth_header) < len("Bearer "):
            flask_restful.abort(401, message="Missing authentication token")
        access_token = auth_header[len("Bearer "):]
        token_info = introspect_token(access_token)
        if not token_info.get("token_is_valid"):
            flask_restful.abort(401, message="Invalid authentication token")
        return fn(*args, **kwargs)
    return wrapper


def get_user(auth_header):
    """
    Takes in an authorization header and returns the authorized user's user_id
    and username. Token is already determined to be valid in Resource before
    this function runs.
    """
    access_token = auth_header[len("Bearer "):]
    token_info = introspect_token(access_token)
    user_info = token_info["user_info"]
    return user_info["user_id"], user_info["username"]


class Example(Resource):
    @classmethod
    @check_bearer_token
    def get(cls):
        """
        Basic example of GET to / using Flask
        """
        user_id, username = get_user(request.headers.get("authorization"))
        num_projects = ProjectModel.get_count()

        # respond
        response_dict = {
            "message":
                f"Hello {username}, there are {num_projects} projects in the database!"
        }
        return Response(
            json.dumps(response_dict), status=200, mimetype="application/json"
        )


class Projects(Resource):
    @classmethod
    @check_bearer_token
    def post(cls):
        """
        Adds Project to database. Ensures json body is valid.
        """
        user_id, username = get_user(request.headers.get("authorization"))
        parser = reqparse.RequestParser()
        parser.add_argument("project_name", type=str, required=True)
        args = parser.parse_args()
        project = ProjectModel(
            owner_id=user_id, owner_username=username, project_name=args["project_name"]
        ).save_to_db()
        return project.json(), 201


class Project(Resource):
    @classmethod
    @check_bearer_token
    def get(cls, project_id):
        """
        Gets the Project in database indicated by the project_id in the url
        and returns a json of it.
        """
        project = ProjectModel.get_by_project_id(project_id)
        if not project:
            return {"message": "Project not found"}, 404
        return project.json(), 200

    @classmethod
    @check_bearer_token
    def delete(cls, project_id):
        """
        Removes the Project in database indicated by the project_id in the url
        and returns a json of the project removed.
        """
        project = ProjectModel.get_by_project_id(project_id)
        if not project:
            return {"message": "Project not found"}, 404
        project_json = project.json()
        project.delete_from_db()
        return project_json, 200


class Comments(Resource):
    @classmethod
    @check_bearer_token
    def post(cls, project_id):
        """
        Adds Comment to database connected to project indicated by the
        project_id in the url. Ensures json body is valid.
        """
        project = ProjectModel.get_by_project_id(project_id)
        if not project:
            return {"message": "Project not found"}, 404
        user_id, username = get_user(request.headers.get("authorization"))
        parser = reqparse.RequestParser()
        parser.add_argument("message", type=str, required=True)
        args = parser.parse_args()
        comment = CommentModel(
            commenter_id=user_id, commenter_username=username, message=args["message"]
        ).save_to_db()
        return comment.json(), 201
