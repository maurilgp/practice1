# Balance de Saldos Insolutos
import decimal, os, logging, pandas, babel
class OutstandingBalance:

    def __init__(self):
        BALANCE = "Balance"
        AMORTIZATION = "Amortization"
        INTERESTS = "Interests"
        TAX_INTERESTS = "Tax Interests"
        PERIOD_PAYMENT = "Period Payment"
        PERIOD_PAYMENT_TAX = "Period Payment W. Taxes"

        balance_list = []
        amortization_list = []
        interests_list = []
        tax_interests_list = []
        period_payment_list = []
        period_payment_tax = []

        self._debt = decimal.Decimal("2400000.00")
        self._annual_interest_rate = decimal.Decimal(".10")
        self._monthly_interest_rate = self._annual_interest_rate / decimal.Decimal(12)
        self._payment_periods = decimal.Decimal("120")
        self._tax_rate = decimal.Decimal(".16")
        self._period_payment = (self._debt * self._monthly_interest_rate) / (decimal.Decimal(1)-(decimal.Decimal(1)+self._monthly_interest_rate)**(-self._payment_periods))



        print("Initial Debt: "+self.us_currency(self._debt))
        print("Annual Interest Rate: " + str(self._annual_interest_rate))
        print("Monthly Interest Rate: " + str(self._monthly_interest_rate))
        print("Number of payment periods: " + str(self._tax_rate))
        print("Period Payment Before Taxes: "+self.us_currency(self._period_payment))

        for i in range(int(self._payment_periods)+1):
            if i == 0:



    def us_currency(self,number):
        return "$"+babel.numbers.format_number(number, locale="en_US")
