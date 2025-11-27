from sqlalchemy import false
from App.models import Position, Staff, Student
from App.database import db
from App.models.shortlist import Shortlist
from sqlalchemy.exc import SQLAlchemyError

def create_shortlist(position_id: int, staff_id: int):
    try:
        staff = Staff.query.get(staff_id)
        position = Position.query.get(position_id)

        if not staff:
            return f"Staff with ID {staff_id} does not exist."
        if not position:
            return f"Position with ID {position_id} does not exist."
        
        existing_shortlist = Shortlist.query.filter_by(position_id=position_id).first()
        if existing_shortlist:
            return f"Shortlist for Position ID {position_id} already exists."
        
        shortlist = Shortlist(position_id=position.id, staff_id=staff.id)
        db.session.add(shortlist)
        db.session.commit()
        return shortlist
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Error creating shortlist: {e}")

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

#add checking for state of position 
def decide_shortlist(student_id, position_id, decision):
    student = db.session.query(Student).filter_by(user_id=student_id).first()
    shortlist = db.session.query(Shortlist).filter_by(student_id=student.id, position_id=position_id, status ="pending").first()
    position = db.session.query(Position).filter(Position.id==position_id, Position.number_of_positions > 0).first()
    if shortlist and position:
        shortlist.update_status(decision)
        position.update_number_of_positions(position.number_of_positions - 1)
        return shortlist
    return False


def get_shortlist_by_student(student_id):
    student = db.session.query(Student).filter_by(user_id=student_id).first()
    return db.session.query(Shortlist).filter_by(student_id=student.id).all()

def get_shortlist_by_position(position_id):
    return db.session.query(Shortlist).filter_by(position_id=position_id).all()
