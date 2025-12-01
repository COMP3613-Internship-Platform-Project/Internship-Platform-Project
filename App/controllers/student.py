from App.models import Student, Position, Employer
from App.database import db
from sqlalchemy.exc import SQLAlchemyError
from App.models.application import Application

def create_student(username: str, password: str, email: str, skills: list):
    try:
        student = Student(username=username, password=password, email=email, skills=skills)
        db.session.add(student)
        db.session.commit()
        return student
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Error creating student: {e}")

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

def view_my_shortlisted_applications(student_id):
    try:
        student: Student | None = Student.query.get(student_id)
        if not student:
            return f"Student with ID {student_id} does not exist."
        
        #retrieve applications in shortlisted state
        applications = Application.query.filter_by(student_id=student.id, state_value="Shortlisted").all()
        result = []
        if applications:
            for application in applications:
                position = application.position
                employer = position.employer if position else None
                result.append({
                    "employer_name": employer.username if employer else None,
                    "position_title": position.title if position else None,
                    "application_status": application.state_value,
                    "student_id": student.id,
                    "student_name": student.username,
                    "student_email": student.email,
                    "student_skills": student.skills if isinstance(student.skills, list) else []
                })
            return result
        else:
            return f"No shortlisted applications found for Student ID {student_id}."
    except SQLAlchemyError as e:
        raise Exception(f"Error retrieving student's shortlist: {e}")

def get_application_by_student_and_position(student_id:int, position_id:int): #Marishel - added function to get application by student ID and position ID
    try:
        student = db.session.query(Student).filter_by(id=student_id).first()
        position = db.session.query(Position).filter_by(id=position_id).first()
        if not student:
            return f"Student with ID {student_id} does not exist."
        if not position:
            return f"Position with ID {position_id} does not exist."
        
        application = db.session.query(Application).filter_by(student_id=student_id, position_id=position_id).first() 
        if application: #Marishel : refactored return 
            return {
                "application_id": application.id,
                "employer_name": db.session.query(Employer).filter_by(id=position.employer_id).first().username,
                "position_title": position.title,
                "application_status": application.state_value,
                "student_email": student.email,
                "student_id": student.id,
                "student_username": student.username,
            }
        else:
            return f"No application found for Student ID {student_id} and Position ID {position_id}."
    except SQLAlchemyError as e:
        raise Exception(f"Error retrieving application: {e}")


def student_reject_position(student_id, position_id):
    try:
        student: Student | None = Student.query.get(student_id)
        if not student:
            return f"Student with ID {student_id} does not exist."
        
        application = Application.query.filter_by(student_id=student.id, position_id=position_id).first()
        if not application:
            return f"No application found for Student ID {student_id} and Position ID {position_id}."
        
        if application.state_value != "Accepted":
            return f"Application is not in an accepted state; cannot reject."
        
        application.state.reject(application)
        db.session.commit()
        return f"Student ID {student_id} has rejected Position ID {position_id}."
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Error processing rejection: {e}")