from App.models import Position, Employer
from App.database import db

def open_position(user_id, title, number_of_positions=1):
    employer = Employer.query.filter_by(user_id=user_id).first()
    if not employer:
        return None
    
    new_position = Position(title=title, number=number_of_positions, employer_id=employer.id)
    db.session.add(new_position)
    try:
        db.session.commit()
        return new_position
    except Exception as e:
        db.session.rollback()
        return None

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
