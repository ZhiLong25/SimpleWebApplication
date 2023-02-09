class Cart():
    def __init__(self, id ,image, prod_name, prod_price, prod_quan):
        self.__prod_id = id
        self.__prod_image = image
        self.__prod_name = prod_name
        self.__prod_price = prod_price
        self.__prod_quan = prod_quan

    def get_product_id(self):
        return self.__prod_id

    def get_image(self):
        return self.__prod_image

    def get_prodname(self):
        return self.__prod_name

    def get_prodprice(self):
        return self.__prod_price

    def get_prodquan(self):
        return self.__prod_quan

    def set_product_id(self, id):
        self.__product_id = id

    def set_image(self, image):
        self.__prod_image = image

    def set_prodname(self, prodname):
        self.__prod_name = prodname

    def set_prodprice(self, prodprice):
        self.__prod_price = prodprice

    def set_prodquan(self, prodquan):
        self.__prod_quan = prodquan
