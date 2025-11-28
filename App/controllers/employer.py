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

def get_shortlisted_applications_for_employer(employer_id: int):
    try:
        employer = Employer.query.get(employer_id)
        if not employer:
            return f"Employer with ID {employer_id} does not exist."

        positions = Position.query.filter_by(employer_id=employer_id).all()
        result = []
        for position in positions:
            # Get applications for the employer's position/s that are in the "Shortlisted" state
            applications = Application.query.filter_by(position_id=position.id, state_value="Shortlisted").all()
            for application in applications:
                student = application.student 
                result.append({
                    "position_id": position.id,
                    "position_title": position.title,
                    "application_status": application.state_value,
                    "student_email": student.email,
                    "student_id": student.id,
                    "student_name": student.username,
                    "student_skills": student.skills if isinstance(student.skills, list) else []
                })
        return result
    except SQLAlchemyError as e:
        raise Exception(f"Error retrieving shortlisted applications: {e}")

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
        
        # Check if application is in Shortlisted state
        if application.state_value != "Shortlisted":
            return "Only shortlisted applications can be accepted."

        # change application state to Accepted
        try:
            application.state.accept(application)
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
        
        # Check if application is in Shortlisted state
        if application.state_value != "Shortlisted":
            return "Only shortlisted applications can be rejected."
        
        # change application state to Rejected
        try:
            application.state.reject(application)
            db.session.add(application)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return f"Error updating application status: {e}"
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Error rejecting student: {e}")