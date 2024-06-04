from classes.ticket import Ticket
from classes.airplane import Airplane

class Passenger:
    def __init__(self, name: str):
        self.name = name
        self.ticket = None
        self.is_serviced = False

    def register(self, ticket: Ticket, airplane: Airplane):
        self.ticket = ticket
        if len(airplane.capacity) > 0:
            airplane.capacity.pop()
            airplane.passengers.append(self)
            return True
        else:
            return False

    def log_info(self):
        print(f"Name: {self.name}")
        print(f"Ticket: {self.ticket}")