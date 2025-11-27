from App.database import db
from App.models import User

class Staff(User):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    shortlist = db.relationship('Shortlist', backref='staff', lazy=True)

    __mapper_args__ = {'polymorphic_identity': 'staff'}

    def __init__(self, username, password, email):
        super().__init__(username=username, password=password, email=email)

    def get_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'type': 'staff'
        }

    def __repr__(self):
        return f"<Staff with ID {self.id} and username {self.username}>"
    