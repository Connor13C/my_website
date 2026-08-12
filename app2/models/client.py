from db import db


class ClientModel(db.Model):
    """Class representation of client table in database.

    Client table has name column which is unique. Has relationship to request
    table and allows for easy sorting of requests."""
    __tablename__ = 'client'

    name = db.Column(db.String(80), primary_key=True)

    requests = db.relationship('RequestModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        """Returns json of client and all requests tied to client."""
        return {'name': self.name, 'requests': [
            request.json() for request in self.requests.all()]}

    @classmethod
    def find_all(cls):
        """Returns all clients and their requests."""
        return cls.query.all()

    @classmethod
    def select(cls, name):
        """Returns client matching name given."""
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        """Saves client to database."""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Deletes client from the database"""
        db.session.delete(self)
        db.session.commit()
