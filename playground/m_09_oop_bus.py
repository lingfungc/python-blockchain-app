from m_09_oop_vehicle import Vehicle


class Bus(Vehicle):
    # * We can add some custom Attriute for Bus Class
    def __init__(self, starting_speed=10):
        # Inherit the Vehicle Attributes
        super().__init__(starting_speed)
        self.passengers = []

    def add_group(self, passengers):
        self.passengers.extend(passengers)


bus_1 = Bus(25)

bus_1.add_warning('Bus testing')
bus_1.get_warnings()

bus_1.add_group(['Sam', 'Joe', 'Sandy'])

print(bus_1.passengers)

bus_1.drive()
