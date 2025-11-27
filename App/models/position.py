from App.database import db
from App.states import OpenState

class Position(db.Model):
    __tablename__ = 'position'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    number_of_positions = db.Column(db.Integer, default=1) #position closes after this number is filled
    status = db.Column(db.String(50), nullable=False, default="Open") #implement state design pattern 
    state=None #state object to handle state-specific behavior
    employer_id = db.Column(db.Integer, db.ForeignKey('employer.id'), nullable=False)
    
    employer = db.relationship("Employer", back_populates="positions")

    def __init__(self, title, employer_id, number):
        self.title = title
        self.employer_id = employer_id
        self.state = OpenState() #initial state
        self.number_of_positions = number
        
    def toJSON(self):
        return {
            "id": self.id,
            "title": self.title,
            "number_of_positions": self.number_of_positions,
            "status": self.status,
            "employer_id": self.employer_id
        }
    
    def set_State(self, state):
        self.state = state
        self.status = state.state_value
        db.session.add(self)
        db.session.commit()
        
    def close_position(self):
        return self.state.close_position(self)
    
    def reopen_position(self):
        return self.state.reopen_position(self)
    