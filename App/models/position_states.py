from abc import ABC, abstractmethod # for state pattern

class State(ABC):
    # Abstract base class for position states
    
    @abstractmethod
    def close_position(self, position):
        """Close the position."""
        pass

    @abstractmethod
    def reopen_position(self, position):
        """Reopen the position."""
        pass

class OpenState(State): #initial state when employer creates position
    def __init__(self):
        self.state_value = "Open"

    def close_position(self, position): #can only go from open to closed
        position.set_State(ClosedState())
        return True #successfully closed
    
    def reopen_position(self, position):
        raise ValueError("Cannot reopen a position that is already Open.")
    
class ClosedState(State):
    def __init__(self):
        self.state_value = "Closed"

    def close_position(self, position):
        return False #position already closed
    
    def reopen_position(self, position):
        position.set_State(OpenState())
        return True #successfully reopened