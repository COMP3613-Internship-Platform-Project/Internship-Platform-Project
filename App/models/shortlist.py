from App.database import db

class Shortlist(db.Model):
    __tablename__ = 'shortlist'
    id = db.Column(db.Integer, primary_key=True)
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'), nullable=False) #to verify that this shortlist is for a specific position

    applications = db.relationship('Application', back_populates='shortlist', lazy=True)
    
    def __init__(self,position_id):
        self.position_id = position_id

    def toJSON(self):
        return {
            "id": self.id,
            "position_id": self.position_id,
        }
