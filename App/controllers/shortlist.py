from App.models import Position, Staff
from App.database import db
from App.models.shortlist import Shortlist
from sqlalchemy.exc import SQLAlchemyError

def create_shortlist(position_id: int, staff_id: int):
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
        
        shortlist = Shortlist(position_id=position.id, staff_id=staff.id)
        db.session.add(shortlist)
        db.session.commit()
        return shortlist
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Error creating shortlist: {e}")

def get_shortlist_by_staff(staff_id: int): #Marishel - added function to get shortlists by staff ID
    try:
        staff = db.session.get(Staff, staff_id)
        if not staff:
            return f"Staff with ID {staff_id} does not exist."
        
        shortlists = db.session.query(Shortlist).filter_by(staff_id=staff_id).all()
        return [shortlist.toJSON() for shortlist in shortlists]
    except SQLAlchemyError as e:
        raise Exception(f"Error retrieving shortlists: {e}")
    
def get_shortlist_by_position(position_id: int): #Marishel - added function to get shortlists by position ID
    try:
        position = db.session.get(Position, position_id)
        if not position:
            return f"Position with ID {position_id} does not exist."
        
        shortlists = db.session.query(Shortlist).filter_by(position_id=position_id).all()
        return [shortlist.toJSON() for shortlist in shortlists]
    except SQLAlchemyError as e:
        raise Exception(f"Error retrieving shortlists: {e}")