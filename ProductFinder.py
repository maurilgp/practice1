import re, os, openpyxl, logging, sys, msvcrt


class Product:
    def __init__(self, code, description):
        self.code = str(code)
        self.description = str(description).upper()

    def __str__(self):
        return self.code + "\t" + self.description


class ProductFinder:
    def __init__(self):
        self.product_dictionary = {}
        self._load_product_database()
        search_text = ""
        alphabet = "abcdefghijklmnopqrstuvwxyzáéíóúñ".upper()
        while True:
            search_text = input("Enter a product description to find: ").upper()
            products = self.search_products(search_text=search_text)
            self.print_products(products=products)

    def _load_product_database(self):
        filename = "tempfiles\\BASE.xlsx"
        abspath = os.path.abspath(filename)
        logging.debug("Attempting to load file: " + abspath)
        try:
            wb = openpyxl.load_workbook(filename)
            logging.debug("Loading file successful!")
            sheet_names = wb.get_sheet_names()
            logging.debug("Worksheets found: " + str(sheet_names))
            logging.debug("Opening worksheet: " + sheet_names[0])
            ws = wb.get_sheet_by_name(sheet_names[0])
            rows = tuple(ws.rows)
            first_row = True
            for i in rows:
                if first_row:
                    first_row = False
                else:
                    if i[0].value is not None:
                        p = Product(code=str(i[1].value), description=str(i[2].value).upper())
                        self.product_dictionary[p.code] = p
                        logging.debug("Product added to dictionary Code: " + p.code + " Description: " + p.description)
            logging.debug("Product database loaded successfully.")
        except Exception:
            logging.debug("Error attempting to load file: " + filename)


    def search_products(self, search_text):
        products = self.product_dictionary.values()
        found_products = []
        for p in products:
            if p.description.find(search_text) > -1:
                found_products.append(p)
        return found_products

    def print_products(self, products):
        print("Products found: ")
        print("--------------------------------------------")
        i = 0
        for p in products:
            i+=1
            print(str(i)+"\t"+str(p))
        print("--------------------------------------------")
