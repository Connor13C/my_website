from datetime import datetime, timezone

from db import db


class JwtBlocklist(db.Model):
    """Class representation of request table in database.

    Request table has id, priority, target_date, product_area, client_name, client,
    title, and description columns. Id values are unique. Has database relationship
    with client table match client name."""
    __tablename__ = 'jwt_blocklist'
    id = db.Column(db.String(36), primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    def __init__(self, id):
        self.id=id

    def json(self):
        """Returns json object of request table row."""
        return {
            'id': self.id
        }

    @classmethod
    def find_by_id(cls, _id):
        """Returns request matching id given."""
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        """Saves request to the database."""
        db.session.add(self)
        db.session.commit()
