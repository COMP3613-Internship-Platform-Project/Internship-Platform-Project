from App.database import db
from App.models import Employer
from sqlalchemy.exc import SQLAlchemyError

def create_employer(username: str, password: str, email: str):
    try:
        employer = Employer(username=username, password=password, email=email)
        db.session.add(employer)
        db.session.commit()
        return employer
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Error creating employer: {e}")