from flask_restful import Resource
from flask import render_template, Response


class Index(Resource):
    """Request endpoint for url /"""
    @staticmethod
    def get():
        """Get endpoint for main page returns html."""
        return Response(render_template('index.html'), mimetype='text/html')
