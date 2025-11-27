from App.database import db
from App.models import Position, Student, Application, Staff
from App.models.shortlist import Shortlist
from sqlalchemy.exc import SQLAlchemyError

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
    
# MOVED FROM shortlist.py

#add checking for state of position 
def add_student_to_shortlist(student_id, position_id, staff_id):
    teacher = db.session.query(Staff).filter_by(user_id=staff_id).first()
    student = db.session.query(Student).filter_by(user_id=student_id).first()
    if student == None or teacher == None:
        return False
    list = db.session.query(Shortlist).filter_by(student_id=student.id, position_id=position_id).first()
    position = db.session.query(Position).filter(
        Position.id == position_id,
        Position.number_of_positions > 0,
        Position.status == "open"
    ).first()
    if teacher and not list and position:
        shortlist = Shortlist(student_id=student.id, position_id=position.id, staff_id=teacher.id, title=position.title)
        db.session.add(shortlist)
        db.session.commit()
        return shortlist
    return False