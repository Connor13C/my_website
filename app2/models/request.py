from db import db


class RequestModel(db.Model):
    """Class representation of request table in database.

    Request table has id, priority, target_date, product_area, client_name, client,
    title, and description columns. Id values are unique. Has database relationship
    with client table match client name."""
    __tablename__ = 'request'

    id = db.Column(db.Integer, primary_key=True)
    priority = db.Column(db.Integer)
    target_date = db.Column(db.String(20))
    product_area = db.Column(db.String(20))
    client_name = db.Column(db.String, db.ForeignKey('client.name'))
    client = db.relationship('ClientModel')
    title = db.Column(db.String(80))
    description = db.Column(db.String)

    def __init__(
            self,
            priority,
            target_date,
            product_area,
            client_name,
            title,
            description):
        self.priority = priority
        self.target_date = target_date
        self.product_area = product_area
        self.client_name = client_name
        self.title = title
        self.description = description

    def json(self):
        """Returns json object of request table row."""
        return {
            'id': self.id,
            'priority': self.priority,
            'target_date': self.target_date,
            'product_area': self.product_area,
            'client_name': self.client_name,
            'title': self.title,
            'description': self.description}

    @classmethod
    def find_all(cls):
        """Returns all requests in request table"""
        return cls.query.all()

    @classmethod
    def select_by_name(cls, client_name):
        """Returns list of all requests with matching client name."""
        return cls.query.filter_by(client_name=client_name)

    @classmethod
    def select_by_id(cls, _id):
        """Returns request matching id given."""
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def select_same_priority(cls, client_name, priority):
        """Returns request matching both client name and priority given."""
        return cls.query.filter_by(
            client_name=client_name,
            priority=priority).first()

    def save_to_db(self):
        """Saves request to the database."""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Deletes the request from the database."""
        db.session.delete(self)
        db.session.commit()
