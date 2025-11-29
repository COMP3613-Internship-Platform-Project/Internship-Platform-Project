from App.models import Student, Shortlist
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

def view_my_applications(student_id):
    try:
        student: Student | None = Student.query.get(student_id)
        if not student:
            return f"Student with ID {student_id} does not exist."
        
        applications = Application.query.filter_by(student_id=student.id).all()
        result = []
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
    except SQLAlchemyError as e:
        raise Exception(f"Error retrieving student's applications: {e}")

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