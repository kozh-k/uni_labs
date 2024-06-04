import unittest
from classes.airplane import Airplane
from classes.crew import Crew
from classes.ticket import Ticket
from classes.passenger import Passenger
from classes.service import Service
from classes.runway import Runway


class TestAirplane(unittest.TestCase):
    def setUp(self):
        tickets = [Ticket(1, 1), Ticket(2, 1), Ticket(3, 2)]
        self.airplane = Airplane(1, tickets)

    def test_refuel(self):
        self.assertEqual(self.airplane.refuel(), 1000)

    def test_takeoff_with_enough_fuel_and_passengers(self):
        crew = Crew()
        crew.safety_is_checked = True
        crew.route_is_planned = True
        self.airplane.fuel = 2000
        self.airplane.passengers = [Passenger("John")]
        self.airplane.takeoff(crew)
        self.assertEqual(self.airplane.fuel, 2000)

    def test_takeoff_insufficient_fuel(self):
        crew = Crew()
        crew.safety_is_checked = True
        crew.route_is_planned = True
        self.airplane.fuel = 500
        self.airplane.passengers = [Passenger("John")]
        self.airplane.takeoff(crew)
        self.assertEqual(self.airplane.fuel, 500)

    def test_takeoff_empty_airplane(self):
        crew = Crew()
        crew.safety_is_checked = True
        crew.route_is_planned = True
        self.airplane.fuel = 2000
        self.airplane.passengers = []
        self.airplane.takeoff(crew)
        self.assertEqual(self.airplane.fuel, 2000)

    def test_land_all_passengers_serviced(self):
        passenger = Passenger("John")
        passenger.is_serviced = True
        self.airplane.passengers = [passenger]
        self.airplane.land()
        self.assertEqual(self.airplane.passengers, [passenger])

    def test_land_not_all_passengers_serviced(self):
        passenger1 = Passenger("John")
        passenger1.is_serviced = True
        passenger2 = Passenger("Alice")
        self.airplane.passengers = [passenger1, passenger2]
        self.airplane.land()
        self.assertEqual(self.airplane.passengers, [passenger1, passenger2])

class TestPassenger(unittest.TestCase):
    def setUp(self):
        self.passenger = Passenger("John")

    def test_register(self):
        ticket = Ticket(1, 1)
        airplane = Airplane(1, [ticket])
        self.passenger.register(ticket, airplane)
        self.assertEqual(self.passenger.ticket, ticket)
        self.assertEqual(airplane.capacity, [])
        self.assertEqual(airplane.passengers, [self.passenger])


class TestService(unittest.TestCase):
    def setUp(self):
        self.service = Service()

    def test_do_service(self):
        passenger1 = Passenger("John")
        passenger2 = Passenger("Alice")
        passengers = [passenger1, passenger2]
        self.service.do_service(passengers)
        self.assertTrue(passenger1.is_serviced)
        self.assertTrue(passenger2.is_serviced)


class TestCrew(unittest.TestCase):
    def setUp(self):
        self.crew = Crew()

    def test_plan_route(self):
        runway = Runway()
        self.crew.plan_route("Destination", "Departure Point", "Departure Time", 1000, runway)
        self.assertTrue(self.crew.route_is_planned)

    def test_ensure_safety(self):
        self.crew.ensure_safety()
        self.assertTrue(self.crew.safety_is_checked)


if __name__ == '__main__':
    unittest.main()