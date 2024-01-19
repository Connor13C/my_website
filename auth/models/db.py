import uuid
from db import db


class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def json(self):
        return {'id': self.id, 'username': self.username}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.remove(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()


class ProjectModel(db.Model):
    """SQL database table project."""
    __tablename__ = "project"

    project_id = db.Column(db.String(120), primary_key=True)
    owner_id = db.Column(db.String(120), nullable=False)
    owner_username = db.Column(db.String(120), nullable=False)
    project_name = db.Column(db.String(120), nullable=False)
    comments = db.relationship("CommentModel",
                               lazy="dynamic",
                               cascade="all, delete-orphan")

    def __init__(self, owner_id, owner_username, project_name):
        self.project_id = str(uuid.uuid4())
        self.owner_id = owner_id
        self.owner_username = owner_username
        self.project_name = project_name

    def json(self):
        return {"project_id": self.project_id,
                "owner_id": self.owner_id,
                "owner_username": self.owner_username,
                "project_name": self.project_name,
                "comments": [comment for comment in self.comments.all()]}

    @classmethod
    def get_by_project_id(cls, project_id: str) -> "ProjectModel":
        """Returns ProjectModel object matching the project_id."""
        return cls.query.filter_by(project_id=project_id).first()

    @classmethod
    def get_all(cls):
        """Returns all ProjectModel objects"""
        return cls.query.filter_by()

    @classmethod
    def get_count(cls) -> int:
        """Returns a count of all projects in project table."""
        return cls.query.count()

    def save_to_db(self) -> "ProjectModel":
        """Inserts ProjectModel into database and saves the session."""
        db.session.add(self)
        db.session.commit()
        return self

    def delete_from_db(self) -> None:
        """Removes ProjectModel from database and saves the session."""
        db.session.delete(self)
        db.session.commit()


class CommentModel(db.Model):
    """SQL Database table comment"""
    __tablename__ = "comment"

    project_id = db.Column(db.String(120), db.ForeignKey("project.project_id"))
    comment_id = db.Column(db.String(120), primary_key=True)
    commenter_id = db.Column(db.String(120), nullable=False)
    commenter_username = db.Column(db.String(120), nullable=False)
    message = db.Column(db.String, nullable=False)

    def __init__(self, commenter_id, commenter_username, message):
        self.comment_id = str(uuid.uuid4())
        self.commenter_id = commenter_id
        self.commenter_username = commenter_username
        self.message = message

    def json(self):
        return {"comment_id": self.comment_id,
                "commenter_id": self.commenter_id,
                "commenter_username": self.commenter_username,
                "message": "message"}

    @classmethod
    def get_by_project_id(cls, project_id: str) -> "CommentModel":
        """Returns CommentModel object matching the id."""
        return cls.query.filter_by(project_id=project_id)

    @classmethod
    def get_count(cls) -> int:
        """Returns a count of all comments in comment table."""
        return cls.query.count()

    def save_to_db(self) -> "CommentModel":
        """Inserts CommentModel into database and saves the session."""
        db.session.add(self)
        db.session.commit()
        return self

    def delete_from_db(self) -> None:
        """Removes CommentModel from database and saves the session."""
        db.session.delete(self)
        db.session.commit()
