from User import *

class Admin(User):
    def __init__(self, first_name, last_name, gender, username, password, email, phoneno, role):
        super().__init__(first_name, last_name, gender, username, password, email, phoneno)
        self.__role = role

    def get_role(self):
        return self.__role

    def set_role(self, role):
        self.__role = role
