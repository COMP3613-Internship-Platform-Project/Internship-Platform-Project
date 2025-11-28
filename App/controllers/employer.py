from App.database import db
from App.models import Employer
from sqlalchemy.exc import SQLAlchemyError

from App.models.application import Application
from App.models.position import Position
from App.models.shortlist import Shortlist
from App.models.student import Student
from App.models.application_states import AcceptedState, RejectedState


def create_employer(username: str, password: str, email: str):
    try:
        employer = Employer(username=username, password=password, email=email)
        db.session.add(employer)
        db.session.commit()
        return employer
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Error creating employer: {e}")

def view_shortlist(employer_id: int, position_id: int):
    try:
        #ensure employer and position exist and are related
        employer: Employer | None = Employer.query.get(employer_id)
        if not employer:
            return f"Employer with ID {employer_id} does not exist."
        
        position: Position | None = Position.query.get(position_id)
        if not position:
            return f"Position with ID {position_id} does not exist."
        
        if position.employer_id != employer.id:
            return f"Employer with ID {employer_id} is not authorized to view the shortlist for this position."
        
        # retrieve shortlist
        shortlists = Shortlist.query.filter_by(position_id=position.id).all()
        return [shortlist.toJSON() for shortlist in shortlists]
    except SQLAlchemyError as e:
        raise Exception(f"Error retrieving shortlist: {e}")

def accept_student(employer_id: int, position_id: int, student_id: int):
    try:
        #ensure employer, position, student and shortlist exist and are related
        employer: Employer | None = Employer.query.get(employer_id)
        if not employer:
            return f"Employer with ID {employer_id} does not exist."
        
        position: Position | None = Position.query.get(position_id)
        if not position:
            return f"Position with ID {position_id} does not exist."
        
        if position.employer_id != employer.id:
            return f"Employer with ID {employer_id} is not authorized to accept students for this position."
        
        student: Student | None = Student.query.get(student_id)
        if not student:
            return f"Student with ID {student_id} does not exist."
        
        application: Application | None = Application.query.filter_by(position_id=position.id, student_id=student.id).first()
        if not application:
            return f"Student with ID {student_id} did not apply for Position ID {position_id}."
        
        try:
            application.state = AcceptedState()
            db.session.add(application)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return f"Error updating application status: {e}"        
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Error accepting student: {e}")

def reject_student(employer_id: int, position_id: int, student_id: int):
    try:
        #ensure employer, position, student and shortlist exist and are related
        employer: Employer | None = Employer.query.get(employer_id)
        if not employer:
            return f"Employer with ID {employer_id} does not exist."
        
        position: Position | None = Position.query.get(position_id)
        if not position:
            return f"Position with ID {position_id} does not exist."
        
        if position.employer_id != employer.id:
            return f"Employer with ID {employer_id} is not authorized to reject students for this position."
        
        student: Student | None = Student.query.get(student_id)
        if not student:
            return f"Student with ID {student_id} does not exist."
        
        application = Application.query.filter_by(position_id=position.id, student_id=student.id).first()
        if not application:
            return f"Student with ID {student_id} did not apply for Position ID {position_id}."
        
        try:
            application.state = RejectedState()
            db.session.add(application)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return f"Error updating application status: {e}"
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Error rejecting student: {e}")