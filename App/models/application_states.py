from App.database import db
from App.models.user import Position
from abc import ABC, abstractmethod # for state pattern

class State(ABC):
    # Abstract base class for application states

    @abstractmethod
    def shortlist(self, application):
        """Shortlist the application."""
        pass
    
    @abstractmethod
    def reject(self, application):
        """Reject the application."""
        pass

    @abstractmethod
    def accept(self, application):
        """Accept the application."""
        pass


class AppliedState(State): #inital state when student creates application 

    def __init__(self):
        self.state_value = "Applied"

    def shortlist(self, application): #can only go from applied to shortlisted
        application.set_State(ShortlistedState())
        return True #successfully shortlisted

    def reject(self, application):
        raise ValueError("Cannot reject an application that is in Applied state.")

    def accept(self, application):
        raise ValueError("Cannot accept an application that is in Applied state.")