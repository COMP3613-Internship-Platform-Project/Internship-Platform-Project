from App.database import db
from abc import ABC, abstractmethod # for state pattern

class State(ABC):
    # Abstract base class for position states
    
    @abstractmethod
    def close_position(self, position):
        """Close the position."""
        pass

    @abstractmethod
    def fill_position(self, position):
        """Fill the position."""
        pass

class OpenState(State): #initial state when employer creates position
    def __init__(self):
        self.state_value = "Open"

    def close_position(self, position): #can only go from open to closed
        position.set_State(ClosedState())
        return True #successfully closed