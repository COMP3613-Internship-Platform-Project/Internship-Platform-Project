from App.database import db
from App.models.application_states import AppliedState, ShortlistedState, RejectedState, AcceptedState
from sqlalchemy.orm import reconstructor

#Converted this class to the Application Class

class Application(db.Model):
    __tablename__ = 'application'
    id=db.Column(db.Integer, primary_key=True)
    student_id=db.Column(db.Integer, db.ForeignKey('student.id', ondelete='CASCADE'), nullable=False)
    position_id=db.Column(db.Integer, db.ForeignKey('position.id', ondelete='CASCADE'), nullable=False)
    shortlist_id=db.Column(db.Integer, db.ForeignKey('shortlist.id'), nullable=True)
    state_value=db.Column(db.String(50), nullable=False, default="Applied")
    state = None  # State object to handle state-specific behavior

    student = db.relationship('Student', back_populates='applications', lazy=True)
    position = db.relationship('Position', backref='applications', lazy=True)
    shortlist = db.relationship('Shortlist', back_populates='applications', lazy=True)
    
    def __init__(self, student_id, position_id):
        self.student_id=student_id
        self.position_id=position_id
        self.state = AppliedState()  # Initial state
        self.state_value = self.state.state_value

    @reconstructor
    def init_on_load(self):
        # Reconstruct the state object based on the stored state_value
        if self.state_value == "Applied":
            self.state = AppliedState()
        elif self.state_value == "Shortlisted":
            self.state = ShortlistedState()
        elif self.state_value == "Rejected":
            self.state = RejectedState()
        elif self.state_value == "Accepted":
            self.state = AcceptedState()
        else:
            self.state = None  # Unknown state

    def toJSON(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "position_id": self.position_id,
            "state": self.state_value
        }
    
    def set_State(self, state):
        self.state = state
        self.state_value = state.state_value
        db.session.add(self)
        db.session.commit()

    def shortlist_application(self):
        return self.state.shortlist_application(self)
    
    def reject(self):
        return self.state.reject(self)
    
    def accept(self):
        return self.state.accept(self)