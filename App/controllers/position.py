from App.models import Position, Employer, Shortlist
from App.database import db
from sqlalchemy.exc import SQLAlchemyError

def create_position(employer_id: int, title: str, number_of_positions: int):
    #check if employer exists
    employer: Employer | None = db.session.get(Employer, employer_id)
    if employer is None:
        return f"Employer with ID {employer_id} does not exist"
    
    existing_position = Position.query.filter_by(employer_id=employer.id, title=title, number_of_positions=number_of_positions).first()

    #preventing duplicate position
    if existing_position:
        return f"Internship position already exists"
    
    try:
        position = Position(title=title, employer_id=employer.id, number=number_of_positions)
        db.session.add(position)
        db.session.commit()
        return position
    except SQLAlchemyError as e:
        db.session.rollback() 
        raise Exception(f"Error creating internship position: {e}")

def open_position(employer_id: int, title: str, number_of_positions: int):
    employer: Employer | None = db.session.get(Employer, employer_id)
    if employer is None:
        return f"Employer with ID {employer_id} does not exist"
    
    existing_position = Position.query.filter_by(
        title=title, 
        number_of_positions=number_of_positions, 
        employer_id=employer.id
    ).first()

    if existing_position:
        return f"Internship position already exists"
    
    try:
        position = Position(title=title, employer_id=employer.id, number=number_of_positions)
        db.session.add(position)
        db.session.commit()
        return position
    except SQLAlchemyError as e:
        db.session.rollback() 
        raise Exception(f"Error creating internship position: {e}")

#Marishel - added employer to close position
def close_position(position_id: int, employer_id: int): #Marishel - added employer to close position
    position = db.session.get(Position, position_id)
    if not position:
        return f"Position with ID {position_id} does not exist."    
    
    if position.employer_id != employer_id:
        return f"Employer with ID {employer_id} is not authorized to close this position."
    
    if position.status == "closed":
        return f"Position with ID {position_id} is already closed."
    else:
        position.close_position()
        return f"Position with ID {position_id} has been closed." # not sure to return message or position object
    
def reopen_position(position_id: int, employer_id: int): #Marishel
    position = db.session.get(Position, position_id)
    if not position:
        return f"Position with ID {position_id} does not exist."    
    if position.employer_id != employer_id:
        return f"Employer with ID {employer_id} is not authorized to close this position."
    if position.status == "open":
        return f"Position with ID {position_id} is already open."
    else:
        position.reopen_position()
        return f"Position with ID {position_id} has been reopened." # not sure to return message or position object


#probably don't need this one
def get_positions_by_employer(user_id):
    employer = Employer.query.filter_by(user_id=user_id).first()
    return db.session.query(Position).filter_by(employer_id=employer.id).all()

def get_all_positions_json():
    positions = Position.query.all()
    if positions:
        return [position.toJSON() for position in positions]
    return []

def get_positions_by_employer_json(user_id):
    employer = Employer.query.filter_by(user_id=user_id).first()
    positions = db.session.query(Position).filter_by(employer_id=employer.id).all()
    if positions:
        return [position.toJSON() for position in positions]
    return []

# MOVED FROM shortlist.py

def get_shortlist_by_position(position_id):
    return db.session.query(Shortlist).filter_by(position_id=position_id).all()

    #MOVED FROM MODELS FILE

    # def update_status(self, status):
    #     self.status = status
    #     db.session.commit()
    #     return self.status

    # def update_number_of_positions(self, number_of_positions):
    #     self.number_of_positions = number_of_positions
    #     db.session.commit()
    #     return self.number_of_positions

    # def delete_position(self):
    #     db.session.delete(self)
    #     db.session.commit()
    #     return

    # def list_positions(self):
    #     return db.session.query(Position).all()
