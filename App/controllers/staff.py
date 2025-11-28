from App.database import db
from App.models import Staff, Student, Shortlist, Position, Application
from sqlalchemy.exc import SQLAlchemyError

def create_staff(username: str, password: str, email: str):
    try:
        staff = Staff(username=username, password=password, email=email)
        db.session.add(staff)
        db.session.commit()
        return staff
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Error creating staff: {e}")
    
def list_students(staff_id: int):
    try:
        staff = Staff.query.get(staff_id)
        if not staff:
            return None
        
        students = Student.query.all()
        students_data = []

        for student in students:
            students_data.append(student.get_json())
        return students_data
    except SQLAlchemyError as e:
        return f"Error listing students: {e}"
    
def view_shortlists(staff_id: int):
    try:
        staff = Staff.query.get(staff_id)
        if not staff:
            return None
        
        shortlists = Shortlist.query.all()
        shortlists_data = []

        for shortlist in shortlists:
            position = Position.query.get(shortlist.position_id)
            applications = Application.query.filter_by(position_id=position.id).all()

            employer_name = position.employer.username if position and position.employer else "N/A"
            position_title = position.title if position else "N/A"

            shortlists_data.append({
                "shortlist_id": shortlist.id,
                "employer_username": employer_name,
                "position_id": position.id,
                "position_title": position_title,
            })

            if applications:
                for application in applications:
                    if application.state_value != "Applied":
                        student = Student.query.get(application.student_id)
                        shortlists_data.append({
                            "application_id": application.id,
                            "application_status": application.state_value,
                            "student_email": student.email if student else "N/A",
                            "student_id": student.id if student else None,
                            "student_name": student.username if student else "N/A",
                            "student_skills": student.skills if student else []
                        })
        return shortlists_data
    except SQLAlchemyError as e:
        return f"Error viewing shortlists: {e}"

def view_shortlist_by_position(staff_id: int, position_id: int):
    try:
        staff = Staff.query.get(staff_id)
        if not staff:
            return None
        
        shortlists = Shortlist.query.filter_by(position_id=position_id).all()
        shortlists_data = []

        for shortlist in shortlists:
            position = Position.query.get(shortlist.position_id)
            applications = Application.query.filter_by(position_id=position.id).all()

            employer_name = position.employer.username if position and position.employer else "N/A"
            position_title = f"{position.title} ({position.id})" if position else "N/A"

            shortlists_data.append({
                "shortlist_id": shortlist.id,
                "employer_username": employer_name,
                "position_id": position.id,
                "position_title": position_title,
            })

            if applications:
                for application in applications:
                    if application.state_value != "Applied":
                        student = Student.query.get(application.student_id)
                        shortlists_data.append({
                            "application_id": application.id,
                            "application_status": application.state_value,
                            "student_email": student.email if student else "N/A",
                            "student_id": student.id if student else None,
                            "student_name": student.username if student else "N/A",
                            "student_skills": student.skills if student else []
                        })
        return shortlists_data
    except SQLAlchemyError as e:
        return f"Error viewing shortlist by position: {e}"

def view_applications(staff_id: int):
    try:
        staff = Staff.query.get(staff_id)
        if not staff:
            return None
        
        applications = Application.query.all()
        applications_data = []

        for application in applications:
            position = Position.query.get(application.position_id)
            student = Student.query.get(application.student_id)

            employer_name = position.employer.username if position and position.employer else "N/A"
            position_title = f"{position.title} ({position.id})" if position else "N/A"

            applications_data.append({
                "application_id": application.id,
                "employer_username": employer_name,
                "position_title": position_title,
                "application_status": application.state,
                "application_state_value": application.state_value,
                "student_email": student.email if student else "N/A",
                "student_id": student.id if student else None,
                "student_username": student.username if student else "N/A",
                "student_skills": student.skills if student else []
            })
        return applications_data
    except SQLAlchemyError as e:
        return f"Error viewing applications: {e}"

def view_applications_by_position(staff_id: int, position_id: int):
    try:
        staff = Staff.query.get(staff_id)
        if not staff:
            return None
        
        applications = Application.query.filter_by(position_id=position_id).all()
        applications_data = []

        for application in applications:
            position = Position.query.get(application.position_id)
            student = Student.query.get(application.student_id)

            employer_name = position.employer.username if position and position.employer else "N/A"
            position_title = f"{position.title} ({position.id})" if position else "N/A"

            applications_data.append({
                "application_id": application.id,
                "employer_username": employer_name,
                "position_title": position_title,
                "application_status": application.state_value,
                "student_email": student.email if student else "N/A",
                "student_id": student.id if student else None,
                "student_username": student.username if student else "N/A",
                "student_skills": student.skills if student else []
            })
        return applications_data
    except SQLAlchemyError as e:
        return f"Error viewing applications by position: {e}"

def view_positions(staff_id: int):
    try:
        staff = Staff.query.get(staff_id)
        if not staff:
            return None
        
        positions = Position.query.all()
        positions_data = []

        for position in positions:
            position_json = position.toJSON()
            position_json["company_name"] = position.employer.username if position.employer else "N/A"
            positions_data.append(position_json)
        return positions_data
    except SQLAlchemyError as e:
        return f"Error viewing positions: {e}"
    