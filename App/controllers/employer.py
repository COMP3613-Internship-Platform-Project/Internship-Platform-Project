from App.database import db
from App.models import Employer
from sqlalchemy.exc import SQLAlchemyError

from App.models.application import Application
from App.models.position import Position
from App.models.shortlist import Shortlist
from App.models.student import Student


def create_employer(username: str, password: str, email: str):
    try:
        employer = Employer(username=username, password=password, email=email)
        db.session.add(employer)
        db.session.commit()
        return employer
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Error creating employer: {e}")

def get_all_shortlists_by_employer(employer_id: int): #Marishel - added employer id as employers are the only ones who would view their shortlists
    try:
        employer = db.session.query(Employer).filter_by(id=employer_id).first()
        if not employer:
            return f"Employer with ID {employer_id} does not exist."

        positions = db.session.query(Position).filter_by(employer_id=employer_id).all()
        all_shortlists = []
        for position in positions:
            shortlist = db.session.query(Shortlist).filter_by(position_id=position.id).first()
            if shortlist:
                shortlist_data = {
                    "shortlist_id": shortlist.id,
                    "position_id": position.id,
                    "position_title": position.title,
                    "employer_username": employer.username,
                    "applications": []
                }
                applications = shortlist.applications
                if applications:
                    for application in shortlist.applications:
                        if application.state_value == "Shortlisted":
                            student = db.session.query(Student).filter_by(id=application.student_id).first()
                            shortlist_data["applications"].append({
                                "application_id": application.id,
                                "application_status": application.state_value,
                                "student_id": student.id,
                                "student_username": student.username,
                                "student_email": student.email,
                                "student_skills": student.skills
                            })
                        else:
                            return {"error": f"Application ID {application.id} is not in Shortlisted state."}
                    all_shortlists.append(shortlist_data)
                if not applications:
                    shortlist_data["applications"] = "No applications in this shortlist." #Marishel - added message for no applications in shortlist
                    all_shortlists.append(shortlist_data)          
        return all_shortlists     
    except SQLAlchemyError as e:
        raise Exception(f"Error retrieving shortlists: {e}")

def get_shortlist_by_position_employer(position_id: int, employer_id: int): #Marishel - added employer to see shortlists for their ONE position
    try:
        employer = db.session.query(Employer).filter_by(id=employer_id).first()
        if not employer:
            return {"error": f"Cannot retrieve shortlist. Employer with ID {employer_id} does not exist."}
        
        position = db.session.query(Position).filter_by(id=position_id, employer_id=employer_id).first()
        if not position:
            return {"error": f"Position with ID {position_id} does not exist for Employer ID {employer_id}."}

        shortlist = db.session.query(Shortlist).filter_by(position_id=position_id).first()
        if not shortlist:
            return {"error": f"Shortlist for Position ID {position_id} does not exist."}

        shortlist_data = {
            "shortlist_id": shortlist.id,
            "position_id": position.id,
            "position_title": position.title,
            "employer_username": position.employer.username,
            "applications": []
        }

        if not shortlist.applications:
            shortlist_data["applications"] = "No applications in this shortlist."
            return shortlist_data

        for application in shortlist.applications:
            if application.state_value == "Shortlisted":
                student = db.session.query(Student).filter_by(id=application.student_id).first()
                shortlist_data["applications"].append({
                    "application_id": application.id,
                    "employer_id": position.employer_id,
                    "application_status": application.state_value,
                    "student_email": student.email,
                    "student_id": student.id,
                    "student_username": student.username,
                    "student_skills": student.skills
                })
            else:
                return {"error": f"Application ID {application.id} is not in Shortlisted state."}
        return shortlist_data

    except SQLAlchemyError as e:
        raise Exception(f"Error retrieving shortlists: {e}")

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
            return f"Application for Student ID {student_id} to Position ID {position_id} has been accepted."
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
            return f"Application for Student ID {student_id} to Position ID {position_id} has been rejected."
        except Exception as e:
            db.session.rollback()
            return f"Error updating application status: {e}"
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Error rejecting student: {e}")