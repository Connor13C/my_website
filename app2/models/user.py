from db import db


class UserModel(db.Model):
    """Class representation of user table in database.

    User table has id, username and password columns. Id and username values
    are unique."""
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def json(self):
        """Returns json object of user without password for security purposes."""
        return {'id': self.id, 'username': self.username}

    def save_to_db(self):
        """Saves user to database."""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Deletes user from database"""
        db.session.remove(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        """Returns user matching username given."""
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        """Returns user matching id given."""
        return cls.query.filter_by(id=_id).first()
