from App.models import Student, Shortlist
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

# Moved from shortlist.py
def get_shortlist_by_student(student_id):
    student = db.session.query(Student).filter_by(user_id=student_id).first()
    return db.session.query(Shortlist).filter_by(student_id=student.id).all()

