class Delivery():
    def __init__(self, first_name, last_name, gender, email, phoneno, address, postal):

        self.__first_name = first_name
        self.__last_name = last_name
        self.__gender = gender
        self.__email = email
        self.__phoneno = phoneno

        self.__address = address
        self.__postal = postal


    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_gender(self):
        return self.__gender

    def get_email(self):
        return self.__email

    def get_phone_number(self):
        return self.__phoneno

    def get_address(self):
        return self.__address

    def get_postal(self):
        return self.__postal


    # MUTATOR
    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_gender(self, gender):
        self.__gender = gender

    def set_email(self,email):
        self.__email=email

    def set_phone_number(self,phoneno):
        self.__phoneno=phoneno

    def setaddress(self, address):
        self.__address = address

    def setpostal(self, postal):
        self.__postal = postal

