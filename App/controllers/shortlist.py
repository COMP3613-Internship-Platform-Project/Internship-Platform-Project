from App.models import Position, Staff, Student
from App.database import db
from App.models.shortlist import Shortlist
from sqlalchemy.exc import SQLAlchemyError

def create_shortlist(position_id: int, staff_id: int): #Marishel - still kept staff id to create as only staff could shortlist
    try:
        staff = Staff.query.get(staff_id)
        position = Position.query.get(position_id)

        if not staff:
            return f"Staff with ID {staff_id} does not exist."
        if not position:
            return f"Position with ID {position_id} does not exist."
        
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

# def get_shortlist_by_staff(staff_id: int): # Marishel - commented out function to get shortlists by staff ID
#     try:
#         staff = db.session.get(Staff, staff_id)
#         if not staff:
#             return f"Staff with ID {staff_id} does not exist."
#         shortlists = db.session.query(Shortlist).filter_by(staff_id=staff_id).all()
#         return [shortlist.toJSON() for shortlist in shortlists]
#     except SQLAlchemyError as e:
#         raise Exception(f"Error retrieving shortlists: {e}")
    
def get_shortlist_by_position(position_id: int): #Marishel - added function to get shortlists by position ID
    try:
        position = db.session.get(Position, position_id)
        if not position:
            return f"Position with ID {position_id} does not exist."
        shortlist = db.session.query(Shortlist).filter_by(position_id=position_id).all()
        applications = shortlist.applications  # Accessing related applications
        shortlist_applications = []
        for application in applications:
            student = db.session.query(Student).filter_by(id=application.student_id).first()
            shortlist_applications.append({
                "application_id": application.id,
                "employer_id": position.employer_id,
                "position_title": position.title,
                "application_status": application.state_value,
                "student_email": student.email,
                "student_id": student.id,
                "student_username": student.username,
            })
        
    except SQLAlchemyError as e:
        raise Exception(f"Error retrieving shortlists: {e}")
    
def get_all_shortlists(): #Marishel - added function to get all shortlists with their applications
    try:
        shortlists = db.session.query(Shortlist).all()
        all_shortlists = []
        for shortlist in shortlists:
            shortlist_applications = shortlist.applications  # Accessing related applications
            applications_data = get_all_shortlists(shortlist.position_id)
            all_shortlists.append({
                "shortlist_id": shortlist.id,
                "position_id": shortlist.position_id,
                "applications": applications_data
            })
        return all_shortlists     
    except SQLAlchemyError as e:
        raise Exception(f"Error retrieving shortlists: {e}")