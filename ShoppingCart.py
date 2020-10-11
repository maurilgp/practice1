import re, logging, decimal, babel.numbers, openpyxl

class Currency:
    def __init__(self, str_currency="0"):
        self._decimal_number = decimal.Decimal("0")

        self._ZERO_SIGN = "0"
        self._NEGATIVE_SIGN = "-"
        self._CURRENCY_SIGN = "$"
        self._PERIOD_SIGN = "."
        self._EMPTY_STRING = ""


        self._currency_pattern = r"^-?\$?(\d+.?|\d*\.\d{1,2})$"
        self._number_pattern = r"^(-?)(\$?)(\d*)(\.?)(\d*)$"

        str_currency = str(str_currency)

        logging.debug("Attempting to parse string \""+str_currency+"\" to currency format.")
        search = re.search(self._currency_pattern, str_currency)
        if search is None:
            raise Exception("Error parsing string \""+str_currency+"\"")

        search = re.search(self._number_pattern, str_currency)
        groups = search.groups()
        # Extract the integer number.
        #self._integer = self._extract_integer(groups[0])
        # Extract the decimal number.
        #self._decimal = self._extract_decimal(groups[2])
        str_number = groups[0]+groups[2]+groups[3]+groups[4]
        logging.debug("Attempting to convert string to Decimal: "+str_number)
        self._decimal_number = decimal.Decimal(str_number)
        logging.debug("Passing successful, currency value: "+self.__str__())


    def add(self, str_decimal):
        decimal_number = decimal.Decimal(str_decimal)
        decimal_result = self._decimal_number + decimal_number
        logging.debug("Addition operation " + str(self._decimal_number) + " + " + str(decimal_number) + " = " + str(decimal_result))
        self._decimal_number = decimal_result

    def substract(self, str_decimal):
        decimal_number = decimal.Decimal(str_decimal)
        decimal_result = self._decimal_number - decimal_number
        logging.debug("Subtraction operation " + str(self._decimal_number) + " - " + str(decimal_number) + " = " + str(decimal_result))
        self._decimal_number = decimal_result

    def muliply(self, str_decimal):
        decimal_number = decimal.Decimal(str_decimal)
        decimal_result = self._decimal_number * decimal_number
        logging.debug("Multiplication operation " + str(self._decimal_number) + " * " + str(decimal_number) + " = " + str(decimal_result))
        self._decimal_number = decimal_result

    def divide(self, str_decimal):
        decimal_number = decimal.Decimal(str_decimal)
        decimal_result = self._decimal_number / decimal_number
        logging.debug("Division operation " + str(self._decimal_number) + " / " + str(decimal_number) + " = " + str(decimal_result))
        self._decimal_number = decimal_result

    def power(self, str_decimal):
        decimal_number = decimal.Decimal(str_decimal)
        decimal_result = self._decimal_number ** decimal_number
        logging.debug("Power operation " + str(self._decimal_number) + " ^ " + str(decimal_number) + " = " + str(decimal_result))
        self._decimal_number = decimal_result

    def test(self):
        str_currency_list = [".01", "0.01", "11.01", "11.", "11", "-.10", "-0.10", "-11.10", "-11.", "-11", "$.01", "$0.01", "$11.01", "$11.", "$11", "-$.10", "-$0.10", "-$11.10", "-$11.", "-$11"]
        for i in str_currency_list:
            c = Currency(i)
            print(str(c))

        c1 = Currency("999.9")
        c1.add("9999.09")

        c2 = Currency("10")
        c2.add("10")
        c2.substract("10")
        c2.muliply("10")
        c2.divide("10")
        c2.power("10")

    def __str__(self):
        return babel.numbers.format_currency(self._decimal_number, "USD", locale='en_US')


class Product:
    def __init__(self, code, description, price):
        self._code = str(code)
        self._description = str(description)
        self._price = Currency(price)

    def __str__(self):
        return str(self._code)+"\t"+str(self._description)+"\t"+str(self._price)

class ShoppingCartItem(Product):
    def __init__(self, amount, product):
        self._amount = decimal.Decimal(amount)
        super().__init__(product._code, product._description, product._price)

    def get_total(self):
        t = self._amount * self._price._decimal_number
        return Currency(str(t))

    def __str__(self):
        return str(self._amount) + "\t" + str(self._code) + "\t" + str(self._description) + "\t" + str(self._price) + "\t" + str(self.get_total())

class ShoppingCart:
    def __init__(self):
        self._shopping_cart = []
        self._product_database = {}

    def get_total(self):
        total = Currency("0")
        for sci in self._shopping_cart:
            total.add(str(sci.get_total()._decimal_number))
        return total

    def _load_product_database(self):
        database_filename = "tempfiles\\products.xlsx"
        logging.debug("Attemping to LOAD product database database: "+database_filename)
        try:
            wb = openpyxl.load_workbook(database_filename)
            sheet_names = wb.get_sheet_names()
            print(sheet_names)
            ws = wb.get_sheet_by_name("ProductDatabase")
            wstuple = tuple(ws.rows)
            first_line = True
            if len(wstuple) > 0:
                for r in wstuple:
                    str_line = ""
                    if len(r) > 0:
                        if r[0].value != None:
                            try:
                                if first_line:
                                    first_line = False
                                    continue
                                else:
                                    p = Product(code=r[0].value, description=r[1].value, price=r[2].value)
                                    self._product_database[p._code] = p
                                    logging.debug("Product loaded to database: "+str(p))
                            except Exception:
                                logging.debug("Error adding product values code: "+r[0]+" description: "+r[1]+" price: "+r[2])
                        else:
                            break
        except Exception:
            logging.debug("Error attempting to load file: "+database_filename)


    def add_product(self, amount, code):
        logging.debug("Attempting to add product to the cart. Amount: " + str(amount) + "\tCode: " + str(code))
        p = self._product_database.get(code)
        if p is not None:
            logging.debug("Product found: "+str(p))
            self._shopping_cart.append(ShoppingCartItem(amount, p))
        else:
            logging.debug("Product not found. Code: "+str(code))


    def print_product_database(self):
        pdv = self._product_database.values()
        print("Product Database")
        print("Code\tDescription\tPrice")
        for p in pdv:
            print(str(p))


    def print_shopping_cart(self):
        i = 1
        print("Shopping Cart")
        print("Item\tAmount\tCode\tDescription\tPrice\tTotal")
        print("---------------------------------------------------------")
        for sci in self._shopping_cart:
            print(str(i) +"\t"+ str(sci))
            i += 1
        print("---------------------------------------------------------")
        print("Total: "+str(self.get_total()))


    def test(self):
        self._load_product_database()
        print()
        self.print_product_database()
        self.add_product(4, "7501003337887")
        self.add_product(3, "7501073411173")
        print()
        self.print_shopping_cart()

    def __str__(self):
        pass
