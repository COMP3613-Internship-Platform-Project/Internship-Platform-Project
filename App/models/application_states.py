from abc import ABC, abstractmethod # for state pattern

class State(ABC):
    # Abstract base class for application states

    @abstractmethod
    def shortlist_application(self, application):
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

    def shortlist_application(self, application): #can only go from applied to shortlisted
        application.set_State(ShortlistedState())
        return True #successfully shortlisted

    def reject(self, application):
        raise ValueError("Cannot reject an application that is in Applied state.")

    def accept(self, application):
        raise ValueError("Cannot accept an application that is in Applied state.")
    
class ShortlistedState(State): #intermediate state when application is shortlisted by staff

    def __init__(self):
        self.state_value = "Shortlisted"

    def shortlist(self):
        raise ValueError("Application is already in Shortlisted state.")
    
    def reject(self, application): 
        application.set_State(RejectedState())
        return True
    
    def accept(self, application): 
        application.set_State(AcceptedState())
        return True
    
class AcceptedState(State): #final state when application is accepted by employer

    def __init__(self):
        self.state_value = "Accepted"

    def shortlist(self):
        raise ValueError("Cannot shortlist an application that is already Accepted.")

    def reject(self, application): #applcation can be rejected by student when accepted by employer
        application.set_State(RejectedState())
        return True #successfully rejected

    def accept(self):
        raise ValueError("Application is already in Accepted state.")
    
class RejectedState(State): #final state when application is rejected by employer

    def __init__(self):
        self.state_value = "Rejected"

    def shortlist(self):
        raise ValueError("Cannot shortlist an application that is Rejected.")

    def reject(self):
        raise ValueError("Application is already in Rejected state.")

    def accept(self, application):
        raise ValueError("Cannot accept an application that is Rejected.")