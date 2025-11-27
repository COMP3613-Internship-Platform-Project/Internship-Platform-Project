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
            position_title = f"{position.title} ({position.id})" if position else "N/A"

            if applications:
                for application in applications:
                    student = Student.query.get(application.student_id)
                    shortlists_data.append({
                        "shortlist_id": shortlist.id,
                        "staff_id": shortlist.staff_id,
                        "company_name": employer_name,
                        "position": position_title,
                        "student_id": student.id if student else None,
                        "student_name": student.username if student else "N/A",
                        "student_email": student.email if student else "N/A",
                        "application_status": application.state_value
                    })
        return shortlists_data
    except SQLAlchemyError as e:
        return f"Error viewing shortlists: {e}"
    
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
    