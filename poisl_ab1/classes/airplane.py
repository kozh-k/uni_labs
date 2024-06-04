from typing import List
from classes.ticket import Ticket
from classes.crew import Crew

class Airplane:
    def __init__(self, id: int, capacity: List[Ticket]):
        def check_id(elem: Ticket):
            return elem.id == id

        self.capacity = list(filter(check_id, capacity))
        self.passengers: List = []
        self.id = id
        self.fuel= 0
        self.tickets = capacity

    def refuel(self):
        try:
            self.fuel += 1000
        except Exception as e:
            print(f"Возникла ошибка при заправке самолета: {e}")
            return None
        return self.fuel

    def takeoff(self, crew: Crew):
        if self.fuel > 1000 and len(self.passengers) > 0 and crew.safety_is_checked and crew.route_is_planned:
            print("Взлетаем!")
            return True
        else:
            print("Недостаточно топлива или пустой самолет!")
            return False

    def land(self):
        for p in self.passengers:
            if not p.is_serviced:
                print("Не все пассажиры обслужены, не садимся")
                return False
        print("Садимся!")
        return True

    def log_info(self):
        print(f"ID: {self.id}")
        print(f"Capacity: {len(self.capacity)-1}")
        print(f"Fuel: {self.fuel}")
        print("Passengers: ")
        for p in self.passengers:
            print(p.name)