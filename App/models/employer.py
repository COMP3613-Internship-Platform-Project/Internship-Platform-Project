from App.database import db
from App.models import User

class Employer(User):
    __tablename__ = 'employer'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    positions = db.relationship("Position", back_populates="employer")

    __mapper_args__ = {'polymorphic_identity': 'employer'}

    def __init__(self, username, password, email):
        super().__init__(username, password, email)

    def get_json(self):
        user_json = super().get_json()
        user_json.update({
            'positions': [position.toJSON() for position in self.positions]
        })
        return user_json
    
    def __repr__(self):
        return f"<Employer {self.username} with ID {self.id}>"