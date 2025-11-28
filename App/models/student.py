from sqlalchemy import JSON
from App.database import db
from App.models import User

class Student(User):
    __tablename__ = 'student'  
    id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True, primary_key=True)
    skills = db.Column(JSON, nullable=False)

    applications = db.relationship('Application', back_populates='student', lazy=True)
   
    __mapper_args__ = {'polymorphic_identity':'student'}    

    def __init__(self, username, password, email, skills):
        super().__init__(username, password, email)
        self.skills = skills

    def get_json(self):
        user_json = super().get_json()
        user_json.update({
            'email': self.email,
            'skills': self.skills
        })
        return user_json

    def __repr__(self):
        return f"<Student {self.username} with ID {self.id}>"
    