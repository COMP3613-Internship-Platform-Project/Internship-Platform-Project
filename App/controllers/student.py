from sqlalchemy import false
from App.models import Position, Student, Application
from App.database import db
from sqlalchemy.exc import SQLAlchemyError

def create_student(username: str, password: str, email: str, skills: list):
    try:
        student = Student(username=username, password=password, email=email, skills=skills)
        db.session.add(student)
        db.session.commit()
        return student
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Error creating student: {e}")

def get_student_by_user_id(user_id):
    return db.session.query(Student).filter_by(user_id=user_id).first()

#need to have States in position to check if position is open or closed
# before creating application 

def create_application(student_id, position_id):
    try:
        student = db.session.query(Student).filter_by(id=student_id).first()
        position = db.session.query(Position).filter_by(id=position_id).first()

        if not student:
            return f"Student with ID {student_id} does not exist."
        if not position:
            return f"Position with ID {position_id} does not exist."

        existing_application = Application.query.filter_by(student_id=student_id, position_id=position_id).first()
        if existing_application:
            return f"Application for Student ID {student_id} to Position ID {position_id} already exists."

        if position.status != "open":
            application = Application(student_id=student.id, position_id=position.id)
            db.session.add(application)
            db.session.commit()
            return application
        else:
            return f"Cannot apply to Position ID {position_id} as it is not open."
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Error creating application: {e}")
