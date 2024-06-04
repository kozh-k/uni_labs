class Ticket:
    def __init__(self, number: int, id: int):
        self.number = number
        self.id = id

    def log_info(self):
        print(f"Number: {self.number}")
        print(f"ID: {self.id}")