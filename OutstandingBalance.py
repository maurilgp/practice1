# Balance de Saldos Insolutos
import decimal, os, logging, pandas
class OutstandingBalance:

    def __init__(self):
        self._debt = decimal.Decimal(2400000.00)
        print(self._debt)
