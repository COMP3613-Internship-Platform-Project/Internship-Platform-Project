from sqlalchemy import false
from App.models import Position, Student
from App.database import db

def get_student_by_user_id(user_id):
    return db.session.query(Student).filter_by(user_id=user_id).first()

#need to have States in position to check if position is open or closed
# before creating application 

def create_application(student_id, position_id):
    student = db.session.query(Student).filter_by(user_id=student_id).first()
    position = db.session.query(Position).filter_by(id=position_id).first()
    application = Application(student_id=student.id, position_id=position.id)
    db.session.add(application)
    db.session.commit()
    return application

