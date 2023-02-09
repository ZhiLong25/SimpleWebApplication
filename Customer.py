import User

class Customer(User.User):
    count_id = 0

    def __init__(self, first_name, last_name, gender, username, password, email, phoneno, joined_date, membership):
        super().__init__(first_name, last_name, gender, username, password, email, phoneno)
        Customer.count_id += 1
        self.__customer_id = Customer.count_id
        self.__joined_date = joined_date
        self.__membership = membership

    # accessor methods
    def get_customer_id(self):
        return self.__customer_id

    def get_joined_date(self):
        return self.__joined_date

    def get_membership(self):
        return self.__membership

    # mutator methods
    def set_customer_id(self, customer_id):
        self.__customer_id = customer_id

    def set_joined_date(self, joined_date):
        self.__joined_date = joined_date

    def set_membership(self, membership):
        self.__membership = membership



