class Products:
    count_id = 0
    # initializer method
    def __init__(self, image, name, description, price, stock, reference):
        Products.count_id += 1
        self.__product_id = Products.count_id
        self.__image = image
        self.__name = name
        self.__description = description
        self.__price = price
        self.__stock = stock
        self.__reference = reference

    # Accessor Method
    def get_product_id(self):
        return self.__product_id

    def get_image(self):
        return self.__image

    def get_name(self):
        return self.__name

    def get_description(self):
        return self.__description

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def get_reference(self):
        return self.__reference

    # Mutator Method

    def set_product_id(self, id):
        self.__product_id = id

    def set_image(self, image):
        self.__image = image

    def set_name(self, name):
        self.__name = name

    def set_description(self, description):
        self.__description = description

    def set_price(self, price):
        self.__price = price

    def set_stock(self, stock):
        self.__stock = stock

    def set_reference(self, reference):
        self.__reference = reference
