from App.models import Position, Staff, Student, Employer
from App.database import db
from App.models.shortlist import Shortlist
from sqlalchemy.exc import SQLAlchemyError

def create_shortlist(position_id: int, staff_id: int): #Marishel - still kept staff id to create as only staff could shortlist
    try:
        position = Position.query.get(position_id)

        if not position:
            return f"Position with ID {position_id} does not exist."
        
        if staff_id:
            staff = Staff.query.get(staff_id)
            if not staff:
                return f"Cannot create shortlist. Staff with ID {staff_id} does not exist."
        
        existing_shortlist = Shortlist.query.filter_by(position_id=position_id).first()
        if existing_shortlist:
            return f"Shortlist for Position ID {position_id} already exists."
        
        # shortlist = Shortlist(position_id=position.id, staff_id=staff.id)
        shortlist = Shortlist(position_id=position.id) # Marishel - removed staff_id from shortlist creation
        db.session.add(shortlist)
        db.session.commit()
        return shortlist
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Error creating shortlist: {e}")

    
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
                "position_title": position.title,
                "application_status": application.state_value,
                "student_email": student.email,
                "student_id": student.id,
                "student_username": student.username,
            })

        return shortlist_data

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
                "position_title": position.title,
                "application_status": application.state_value,
                "student_email": student.email,
                "student_id": student.id,
                "student_username": student.username,
            })

        return shortlist_data

    except SQLAlchemyError as e:
        raise Exception(f"Error retrieving shortlists: {e}")

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
                        })

                    all_shortlists.append(shortlist_data)
                if not applications:
                    shortlist_data["applications"] = "No applications in this shortlist." #Marishel - added message for no applications in shortlist
                    all_shortlists.append(shortlist_data)          
        return all_shortlists     
    except SQLAlchemyError as e:
        raise Exception(f"Error retrieving shortlists: {e}")
    
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
                    })

                all_shortlists.append(shortlist_data)
            if not applications:
                shortlist_data["applications"] = "No applications in this shortlist." #Marishel - added message for no applications in shortlist
                all_shortlists.append(shortlist_data)          
        return all_shortlists     
    except SQLAlchemyError as e:
        raise Exception(f"Error retrieving shortlists: {e}")
    
    
# def get_shortlist_by_staff(staff_id: int): # Marishel - commented out function to get shortlists by staff ID
#     try:
#         staff = db.session.get(Staff, staff_id)
#         if not staff:
#             return f"Staff with ID {staff_id} does not exist."
#         shortlists = db.session.query(Shortlist).filter_by(staff_id=staff_id).all()
#         return [shortlist.toJSON() for shortlist in shortlists]
#     except SQLAlchemyError as e:
#         raise Exception(f"Error retrieving shortlists: {e}")