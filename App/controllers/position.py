from App.models import Position, Employer
from App.database import db
from sqlalchemy.exc import SQLAlchemyError

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
        return f"Error creating internship position: {e}"

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
