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
