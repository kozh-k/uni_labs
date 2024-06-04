from classes.runway import Runway

class Crew:
    def __init__(self):
        self.destination = None
        self.dep_point = None
        self.dep_time = None
        self.route_is_planned = False
        self.plane_id = 0
        self.safety_is_checked = False

    def plan_route(self, destination: str, dep_point: str, dep_time: int, min_runway_length: int, runway: Runway):
        self.destination = destination
        self.dep_point = dep_point
        self.dep_time = dep_time
        if min_runway_length <= runway.length:
            self.route_is_planned = True

    def ensure_safety(self):
        self.safety_is_checked = True

    def log_info(self):
        print(f"Маршрут запланирован: {self.route_is_planned}")
        print(f"Безопастность проверена: {self.safety_is_checked}")