# Balance de Saldos Insolutos
import decimal, os, logging, pandas, babel, sys

class OutstandingBalance:

    def __init__(self):
        PERIOD_PAYMENT = "Period Payment"
        INTERESTS = "Interests"
        TAX_INTERESTS = "Tax Interests"
        AMORTIZATION = "Amortization"
        PERIOD_PAYMENT_TAX = "Period Payment W. Taxes"
        BALANCE = "Balance"

        period_payment_list = []
        interests_list = []
        tax_interests_list = []
        amortization_list = []
        period_payment_tax_list = []
        balance_list = []

        self._debt = decimal.Decimal("2400000.00")
        self._annual_interest_rate = decimal.Decimal(".10")
        self._monthly_interest_rate = round(self._annual_interest_rate / decimal.Decimal(12),3)
        self._payment_periods = decimal.Decimal("120")
        self._tax_rate = decimal.Decimal(".16")
        self._period_payment = (self._debt * self._monthly_interest_rate) / (decimal.Decimal(1)-(decimal.Decimal(1)+self._monthly_interest_rate)**(-self._payment_periods))

        for i in range(int(self._payment_periods)+1):
            if i == 0:
                period_payment_list.append(0)
                interests_list.append(0)
                tax_interests_list.append(0)
                amortization_list.append(0)
                period_payment_tax_list.append(0)
                balance_list.append(self._debt)
            else:
                period_payment_list.append(self._period_payment)
                interests_list.append(balance_list[i-1]*self._monthly_interest_rate)
                tax_interests_list.append(interests_list[i]*self._tax_rate)
                amortization_list.append(period_payment_list[i]-interests_list[i])
                period_payment_tax_list.append(period_payment_list[i]+tax_interests_list[i])
                balance_list.append(balance_list[i-1]-amortization_list[i])

        debt_df = pandas.DataFrame({
        PERIOD_PAYMENT : self._us_currency_list(period_payment_list),
        INTERESTS : self._us_currency_list(interests_list),
        TAX_INTERESTS : self._us_currency_list(tax_interests_list),
        AMORTIZATION : self._us_currency_list(amortization_list),
        PERIOD_PAYMENT_TAX : self._us_currency_list(period_payment_tax_list),
        BALANCE : self._us_currency_list(balance_list)
            }
        )

        os.system("cls")
        print("#####################################################################")
        print("                           BALANCE STATEMENT")
        print("#####################################################################")
        print("Initial Debt: " + self._us_currency(self._debt))
        print("Annual Interest Rate: " + str(self._annual_interest_rate))
        print("Monthly Interest Rate: " + str(self._monthly_interest_rate))
        print("Tax Rate: " + str(self._tax_rate))
        print("Number of payment periods: "+str(self._payment_periods))
        print("Period Payment Before Taxes: " + self._us_currency(self._period_payment))
        print("#####################################################################")
        print(debt_df)

    def _us_currency_list(self, number_list):
        ucl = []
        for i in number_list:
            ucl.append(self._us_currency(i))
        return ucl

    def _us_currency(self, number):
        return babel.numbers.format_currency(round(number, 2), "USD", locale="en_US")
