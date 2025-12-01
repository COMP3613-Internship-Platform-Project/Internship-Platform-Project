from App.database import db
from App.models import Staff, Student, Shortlist, Position, Application, Employer
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
            students_data.append({
                "id": student.id,
                "username": student.username,
                "email": student.email,
                "skills": ", ".join(student.skills) if isinstance(student.skills, list) else str(student.skills),
                "type": "student"
            })
        return students_data
    except SQLAlchemyError as e:
        return f"Error listing students: {e}"

def get_all_shortlists(staff_id: int): #Marishel - added staff id as staff are the only ones who would view all shortlists
    try:
        staff = db.session.query(Staff).filter_by(id=staff_id).first()
        if not staff:
            return f"Staff with ID {staff_id} does not exist."

        shortlists = db.session.query(Shortlist).all()
        all_shortlists = []
        for shortlist in shortlists:
            applications = shortlist.applications
            position = db.session.query(Position).filter_by(id=shortlist.position_id).first()
            employer = db.session.query(Employer).filter_by(id=position.employer_id).first()
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
                    student = db.session.query(Student).filter_by(id=application.student_id).first()
                    shortlist_data["applications"].append({
                        "application_id": application.id,
                        "application_status": application.state_value,
                        "student_id": student.id,
                        "student_username": student.username,
                        "student_email": student.email,
                        "student_skills": student.skills
                    })

                all_shortlists.append(shortlist_data)
            if not applications:
                shortlist_data["applications"] = "No applications in this shortlist." #Marishel - added message for no applications in shortlist
                all_shortlists.append(shortlist_data)          
        return all_shortlists     
    except SQLAlchemyError as e:
        raise Exception(f"Error retrieving shortlists: {e}")

def get_shortlist_by_position_staff(position_id: int, staff_id: int): #Marishel - added staff id as only staff would view shortlists
    try:
        staff = db.session.query(Staff).filter_by(id=staff_id).first()
        if not staff:
            return {"error": f"Cannot retrieve shortlist. Staff with ID {staff_id} does not exist."}

        position = db.session.query(Position).filter_by(id=position_id).first()
        if not position:
            return {"error": f"Position with ID {position_id} does not exist."}

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

        return shortlist_data

    except SQLAlchemyError as e:
        raise Exception(f"Error retrieving shortlists: {e}")

def get_all_applications(staff_id:int): #Marishel - added function to get all applications checking to ensure user is staff
    try:
        staff = db.session.query(Staff).filter_by(id=staff_id).first()
        if not staff:
            return f"Only staff members can access applications. Staff with ID {staff_id} does not exist."
        
        applications = db.session.query(Application).all()
        applications_data = []
        for application in applications:
            student = db.session.query(Student).filter_by(id=application.student_id).first()
            position = db.session.query(Position).filter_by(id=application.position_id).first()
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

def get_applications_by_position(staff_id:int, position_id:int): # Marishel - added function to get applications by position ID and checking to ensure user is staff
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

def view_positions(staff_id: int):
    try:
        staff = Staff.query.get(staff_id)
        if not staff:
            return None
        
        positions = Position.query.all()
        positions_data = []

        for position in positions:
            positions_data.append({
                "id": position.id,
                "title": position.title,
                "number_of_positions": position.number_of_positions,
                "status": position.status if hasattr(position, "status") else "N/A",
                "employer_id": position.employer_id,
                "company_name": position.employer.username if position.employer else "N/A"
            })
        return positions_data
    except SQLAlchemyError as e:
        return f"Error viewing positions: {e}"
    
