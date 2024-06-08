from m_09_oop_vehicle import Vehicle


# * Inherit from Parent Class as an Argument
class Car(Vehicle):
    # * Inheriting Attributes and Methods from Vehicle Class
    # # Adding Attributes (This is a Class Attributes)
    # top_speed = 100

    # def __init__():
    #     pass

    # def drive(self):
    #     # This is NOT working because Python will search for a variable created OUTSIDE of the Class
    #     # print(f'My top speed is {top_speed}')
    #     print(f'My top speed is {self.top_speed}')

    def brag(self):
        print('I am only available in Car Class and its instances. So Cool!')


# We can create a instance of 'car' Class and the 'Car()' here is a Constructor
first_car = Car()
first_car.drive()
print(first_car)

# Update the Class Attribute Value
# Car.top_speed = 200

second_car = Car()
second_car.drive()
print(second_car)

# third_car = Car()
# third_car.drive()
