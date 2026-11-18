class Phone:
    def __init__(self, version, color, storage, price):
        self.version = version
        self.color = color
        self.storage = storage
        self.price = price
    def turn_on(self):
        print(f'{self.version} is turned on.')
    def turn_off(self):
        print(f'{self.version} is turned off.')
    def make_call(self, number):
        print(f'Calling {number} from {self.version}.')
    def send_message(self, number, message):
        print(f'Sending message "{message}" to {number} from {self.version}.')
    def check_battery(self):
        print(f'Checking battery status of {self.version}.')
    def charge_battery(self):
        print(f'Charging battery of {self.version}.')