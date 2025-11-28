from App.controllers.shortlist import create_shortlist
from App.database import db
from App.models import Position, Student, Application, Staff
from App.models.employer import Employer
from App.models.shortlist import Shortlist
from sqlalchemy.exc import SQLAlchemyError
from App.controllers.shortlist import create_shortlist
from App.models.application_states import ShortlistedState

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
    


def add_application_to_shortlist(staff_id, application_id):
    staff = Staff.query.get(staff_id)
    if not staff:
        return f"Staff with ID {staff_id} does not exist."
    application = Application.query.get(application_id)
    if not application:
        return f"Application with ID {application_id} does not exist."
    
    #check if a shortlist exists for the specific position
    shortlist = Shortlist.query.filter_by(position_id=application.position_id).first()
    if not shortlist:
        shortlist = create_shortlist(application.position_id, staff.id)
    
    #check if application is already in shortlist
    existing_entry = Shortlist.query.filter_by(position_id=application.position_id).first()
    if existing_entry and application.shortlist_id == existing_entry.id:
        return f"Application with ID {application_id} is already in the shortlist for Position ID {application.position_id}."
    
    try:
        application.shortlist_id = shortlist.id

        # ensuring application transition strictly from applied to shortlisted state
        if application.state_value == "Applied":
            application.shortlist_application() #there is no state here to change, so causing problems
        else:
            return f"Application with ID {application_id} cannot be shortlisted from state '{application.state_value}'."

        db.session.commit()
        return application
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Error adding application to shortlist: {e}")
    
    
def get_applications_by_student(student_id: int): #Marishel - added function to get applications by student ID
    try:
        student = db.session.get(Student, student_id)
        if not student:
            return f"Student with ID {student_id} does not exist."
        
        applications = db.session.query(Application).filter_by(student_id=student_id).all()
        applications_data = []
        for application in applications:
            position = db.session.query(Position).filter_by(id=application.position_id).first()
            if position: 
                employer = db.session.query(Employer).filter_by(id=position.employer_id).first()
                applications_data.append({
                    "employer_name": employer.username,
                    "position_title": position.title,
                    "application_status": application.state_value,
                    "studnet_email": student.email,
                    "student_id": student.id,
                    "student_username": student.username,
                    "student_skills": student.skills,
                })
        return applications_data
    except SQLAlchemyError as e:
        raise Exception(f"Error retrieving applications: {e}")
    
def get_application_by_student_and_position(student_id:int, position_id:int): #Marishel - added function to get application by student ID and position ID
    try:
        student = db.session.query(Student).filter_by(id=student_id).first()
        position = db.session.query(Position).filter_by(id=position_id).first()
        if not student:
            return f"Student with ID {student_id} does not exist."
        if not position:
            return f"Position with ID {position_id} does not exist."
        
        application = db.session.query(Application).filter_by(student_id=student_id, position_id=position_id).first()
        if application:
            return application.toJSON() #did to json for now 
        else:
            return f"No application found for Student ID {student_id} and Position ID {position_id}."
    except SQLAlchemyError as e:
        raise Exception(f"Error retrieving application: {e}")
    
def get_applications_by_position_staff(staff_id:int, position_id:int): # Marishel - added function to get applications by position ID and checking to ensure user is staff
    try:
        staff = db.session.query(Staff).filter_by(id=staff_id).first()
        if not staff:
            return f"Only staff members can access applications. Staff with ID {staff_id} does not exist."
        position = db.session.query(Position).filter_by(id=position_id).first()
        if not position:
            return f"Position with ID {position_id} does not exist."
        
        applications = db.session.query(Application).filter_by(position_id=position_id).all()
        applications_data = []
        for application in applications:
            student = db.session.query(Student).filter_by(id=application.student_id).first()
            employer = db.session.query(Employer).filter_by(id=position.employer_id).first()
            applications_data.append({
                "application_id": application.id,
                "employer_name": employer.username,
                "position_title": position.title,
                "application_status": application.state_value,
                "student_email": student.email,
                "student_id": student.id,
                "student_username": student.username,
            })
        return applications_data
    except SQLAlchemyError as e:
        raise Exception(f"Error retrieving applications: {e}")