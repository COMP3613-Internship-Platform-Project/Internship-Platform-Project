from App.models import Position, Staff
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
        
        shortlist = Shortlist(position_id=position.id) # Marishel - removed staff_id from shortlist creation
        db.session.add(shortlist)
        db.session.commit()
        return shortlist
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Error creating shortlist: {e}")
