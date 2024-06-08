class Vehicle:
    # Adding Attributes (This is a Class Attributes)
    top_speed = 100

    def __init__(self, starting_speed=30):
        self.start_speed = starting_speed

        # Private Attribute (Only Accessible Inside the Class or by a Method)
        self.__warnings = []

    # Special Method
    def __repr__(self):
        print('Printing ...')
        return 'Start Speed: {}, Warnings: {}'.format(self.start_speed,
                                                      len(self.__warnings))

    # Method to Access Private Attribute (__warnings)
    def add_warning(self, warning_text):
        if len(warning_text) > 0:
            self.__warnings.append(warning_text)

    # Method to Access Private Attribute (__warnings)
    def get_warnings(self):
        return self.__warnings

    def drive(self):
        # This is NOT working because Python will search for a variable created OUTSIDE of the Class
        # print(f'My top speed is {top_speed}')
        print(f'My top speed (Class Attr) is {self.top_speed}')
        print(f'My start speed (Instance Attr) is {self.start_speed}')
