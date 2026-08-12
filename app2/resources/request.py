from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models.request import RequestModel
from models.client import ClientModel
from models.parser import Parser


class Request(Resource):
    """Request endpoint for url/request"""
    @jwt_required()
    def post(self):
        """Post endpoint for adding requests into the database.

        Headers: {Authorization: JWT jwt_token, ContentType: application/json}
        Body must be json with priority, target_date, product_area, client_name,
        title, description fields. Database must have matching client_name or
        will return json message 400 error. If error occurs while inserting into
        database will return json message and 500 error. On successful insert
        into database returns json of request and 201 code."""
        parser = Parser()
        parser.required_fields(
            'priority',
            'target_date',
            'product_area',
            'client_name',
            'title',
            'description')
        data = parser.parse_args()
        if not ClientModel.select(data['client_name']):
            return {
                'message': 'Client does not exist'}, 400
        request = RequestModel(**data)
        client_name = data['client_name']
        priority = data['priority']
        update_list = []
        try:
            while RequestModel.select_same_priority(client_name, priority):
                update_list.append(
                    RequestModel.select_same_priority(
                        client_name, priority))
                priority += 1
            request.save_to_db()
            for req in update_list:
                req.priority += 1
                req.save_to_db()
        except BaseException:
            return {'message': 'Something went wrong'}, 500
        return request.json(), 201


class RequestID(Resource):
    """Request endpoint for url/request/<int:request_id>"""
    @jwt_required()
    def get(self, request_id):
        """Get endpoint for request with matching id in the database.

        Headers: {Authorization: JWT jwt_token, ContentType: application/json}
        If no request with ID found will return json message 404 error. If found
        returns json of request with matching ID and 200 code."""
        request = RequestModel.select_by_id(request_id)
        if request:
            return request.json(), 200
        return {'message': 'Request not found'}, 404

    @jwt_required()
    def delete(self, request_id):
        """Get endpoint for request with matching id in the database.

        Headers: {Authorization: JWT jwt_token, ContentType: application/json}
        If no request with ID found will return json message and 404 error. If
        found and deleted returns 200 code."""
        request = RequestModel.select_by_id(request_id)
        if request:
            request.delete_from_db()
            return {'message': 'Request deleted'}, 200
        return {'message': 'Request not found'}, 404


class RequestList(Resource):
    """Request endpoint for url/requests"""
    @jwt_required()
    def get(self):
        """Get endpoint for all requests.

        Headers: {Authorization: JWT jwt_token, ContentType: application/json}
        Returns json object of all requests and 200 code."""
        return {'requests': [request.json()
                             for request in RequestModel.find_all()]}, 200
