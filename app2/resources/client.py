from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models.client import ClientModel


class Client(Resource):
    """Client endpoint for url/client/<string:name>"""
    @jwt_required()
    def get(self, name):
        """Get endpoint for client name.

        Headers: {Authorization: JWT jwt_token, ContentType: application/json}
        If client name in database not found returns json message 404 error.
        Returns json object of client and all requests with that client name
        and 200 code."""
        client = ClientModel.select(name)
        if client:
            return client.json(), 200
        return {'message': 'Client not found'}, 404

    @jwt_required()
    def post(self, name):
        """Post endpoint for client name.

        Headers: {Authorization: JWT jwt_token, ContentType: application/json}
        If client name already in database returns json message and 400 error.
        If error occurs while adding to database returns 500 error. Returns
        json object of client and empty requests field and 201 code."""
        if ClientModel.select(name):
            return {'message': 'Client already exists'}, 400
        client = ClientModel(name)
        try:
            client.save_to_db()
        except BaseException:
            return {'message': 'Something went wrong'}, 500
        return client.json(), 201

    @jwt_required()
    def delete(self, name):
        """Delete endpoint for client name.

        Headers: {Authorization: JWT jwt_token, ContentType: application/json}
        If client name is not found in database returns json message and 404
        error. Deletes all requests of client and then the client from the
        database and returns json message and 201 code."""
        client = ClientModel.select(name)
        if client:
            for request in client.requests:
                request.delete_from_db()
            client.delete_from_db()
            return {'message': 'Client deleted'}, 200
        return {'message': 'Client not found'}, 404


class Clients(Resource):
    """Request endpoint for url/clients"""
    @jwt_required()
    def get(self):
        """Get endpoint for clients and returns json with client names and 200 code"""
        return {'clients': [client.name
                            for client in ClientModel.find_all()]}, 200
