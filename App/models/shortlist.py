from App.database import db

class Shortlist(db.Model):
    __tablename__ = 'shortlist'
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db,ForeignKey('application.id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)

    applications = db.relationship('Application', backref=db.backref('shortlist', lazy=True))

    def __init__(self, application_id, staff_id):
        self.application_id = application_id
        self.staff_id = staff_id
        #set application state to shorlisted here most likely through a controller or something?


    def toJSON(self):
        return {
            "id": self.id,
            "application_id": self.application_id,
            "staff_id": self.staff_id
        }
