from classes.ticket import Ticket
from classes.airplane import Airplane
from classes.passenger import Passenger
from classes.crew import Crew
from classes.service import Service
from classes.runway import Runway

def check(input_str):
    if input_str.strip() == '':
        print("Ошибка: введена пустая строка. Попробуйте еще раз.")
        return False
    else:
        return True
    
def input_check(text):
    while True:
        user_input = input(text)
        if check(user_input):
            return user_input

def print_menu():
    print("Выберите действие:")
    print("1. Создать самолет")
    # print("2. Создать билет")
    print("3. Создать пассажира")
    print("4. Операция регистрации на рейс")
    print("5. Операция взлета")
    print("6. Операция обслуживания пассажиров в полете")
    print("7. Операция планирования маршрутов")
    print("8. Операция обеспечения безопасности")
    print("9. Операция заправки самолета")
    print("10. Информация о выбранном самолете")
    print("11. Операция посадки")
    print("0. Выход")

def create_airplane(airplanes):
    id = input_check("Введите идентификатор самолета: ")
    capacity = int(input_check("Введите вместимость самолета: "))
    tickets = [Ticket(i + 1, id) for i in range(capacity)]
    airplane = Airplane(id, tickets)
    airplanes.append(airplane)
    print("Самолет успешно создан.")

# def create_ticket(tickets):
#     number = input_check("Введите номер билета: ")
#     id = input_check("Введите идентификатор самолета: ")
#     ticket = Ticket(number, id)
#     tickets.append(ticket)
#     print("Билет успешно создан.")

def create_passenger(passengers):
    name = input_check("Введите имя пассажира: ")
    passenger = Passenger(name)
    passengers.append(passenger)
    print("Пассажир успешно создан.")

def register_passenger(passenger, airplane):
    print(airplane.tickets[0].number)
    ticket_number = int(input_check("Введите номер билета: "))
    ticket = next((t for t in airplane.tickets if t.number == ticket_number), None)
    if ticket:
        passenger.register(ticket, airplane)
        print("Пассажир успешно зарегистрирован на рейс.")
    else:
        print("Билет не найден.")

def takeoff(airplane, crew):
    #airplane.log_info()
    #crew.log_info()
    airplane.takeoff(crew)

def land(airplane):
    #airplane.log_info()
    airplane.land()

def service_passengers(service, passengers):
    service.do_service(passengers)
    print("Пассажиры обслужены.")

def plan_route(crew, runway):
    destination = input_check("Введите пункт назначения: ")
    dep_point = input_check("Введите пункт отправления: ")
    dep_time = input_check("Введите время отправления: ")
    min_runway_length = input_check("Введите минимальную длину взлетно-посадочной полосы: ")

    crew.plan_route(destination, dep_point, dep_time, min_runway_length, runway)
    print("Маршрут запланирован.")

def ensure_safety(crew):
    crew.ensure_safety()
    print("Безопасность проверена.")

def refuel(airplane):
    airplane.refuel()
    print("Самолет заправлен.")

def log_info_airplane(airplane):
    airplane.log_info()

def main():
    airplanes = []
    tickets = []
    passengers = []
    service = Service()
    runway = Runway()
    crew = Crew()

    while True:
        print_menu()
        choice = input_check("Введите номер действия: ")
        if choice == "1":
            create_airplane(airplanes)
        # elif choice == "2":
            # create_ticket(tickets)
        elif choice == "3":
            create_passenger(passengers)
        elif choice == "4":
            if len(airplanes) == 0:
                print("Сначала создайте самолет.")
            else:
                passenger = None
                while passenger is None:
                    passenger_name = input_check("Введите имя пассажира: ")
                    for p in passengers:
                        if p.name == passenger_name:
                            passenger = p
                            break

                    if passenger is None:
                        print("Пассажир не найден.")

                airplane = None
                while airplane is None:
                    airplane_id = input_check("Введите идентификатор самолета: ")
                    for a in airplanes:
                        if a.id == airplane_id:
                            airplane = a
                            break

                    if airplane is None:
                        print("Самолет не найден.")

                register_passenger(passenger, airplane)
        elif choice == "5":
            if len(airplanes) == 0:
                print("Сначала создайте самолет.")
            else:
                crew.log_info()
                airplanes[0].takeoff(crew)
        elif choice == "11":
            airplanes[0].land()
        elif choice == "6":
            if len(passengers) == 0:
                print("Сначала создайте пассажиров.")
            else:
                service_passengers(service, passengers)
        elif choice == "7":
            plan_route(crew, runway)
        elif choice == "8":
            ensure_safety(crew)
        elif choice == "9":
            if len(airplanes) == 0:
                print("Сначала создайте самолет.")
            else:
                refuel(airplanes[0])
        elif choice == "10":
            airplane_id = input("Введите id самолета: ")
            for airplane in airplanes:
                if airplane.id == airplane_id:
                    log_info_airplane(airplane)
        elif choice == "0":
            break
        else:
            print("Некорректный ввод. Попробуйте ещё раз.")

if __name__ == "__main__":
    main()