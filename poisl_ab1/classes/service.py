from typing import List
from classes.passenger import Passenger

class Service:
    def __init__(self):
        self.name = 'Airplane service'

    def do_service(self, passengers: List[Passenger]):
        for passenger in passengers:
            passenger.is_serviced = True