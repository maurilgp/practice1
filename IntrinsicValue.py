import decimal, babel, datetime, pandas

class IntrinsicValue:
    def __init__(self):
        self._company = "Cisco Systems"
        self._ticker = "CSCO"
        self._current_share_price = decimal.Decimal(39.81)
        self._date = datetime.datetime.strptime("2020/10/14", "%Y/%m/%d")
        self._shares_outstanding = decimal.Decimal("4233430000")
        self._free_cash_flow = decimal.Decimal("14656000000")
        self._business_grow_rate_percent = decimal.Decimal("1.55")
        self._business_tax_rate_percent = decimal.Decimal("19.73")
        self._business_interest_rate_percent = decimal.Decimal("3.10")
        self._market_capitalization = decimal.Decimal("168533000000")
        self._beta_coefficient = decimal.Decimal("0.83")
        self._risk_free_rate_percent = decimal.Decimal("0.732")
        self._market_risk_premium_percent = decimal.Decimal("5.6")
        self._long_term_debt = decimal.Decimal("11578000000")
        self._short_term_debt = decimal.Decimal("3005000000")
        self._total_business_cash = decimal.Decimal("29419000000")
        self._gdp_growth_rate_percent = decimal.Decimal("1.26")
        self._total_business_debt = decimal.Decimal("17499600000")

        self._market_value_debt = (self._long_term_debt + self._short_term_debt) * decimal.Decimal("1.20")
        self._cost_equity = self._risk_free_rate_percent + self._beta_coefficient * self._market_risk_premium_percent
        self._cost_debt = self._business_interest_rate_percent * (1 - self._business_tax_rate_percent/decimal.Decimal("100"))
        self._market_value_equity = self._market_capitalization
        self._we = self._market_value_equity / (self._market_value_debt+self._market_value_equity)
        self._wd = self._market_value_debt / (self._market_value_debt+self._market_value_equity)
        self._discount_rate_percent = self._we * self._cost_equity + self._wd * self._cost_debt
        self._years = 10
        self._projected_cash_flow = []
        self._discount_factor = []
        self._discounted_cash_flow = []
        for i in range(self._years):
            y = i+1
            pcf = self._free_cash_flow * \
                  (1 + self._business_grow_rate_percent/decimal.Decimal("100")) \
                  ** y
            df = 1 / (1 + self._discount_rate_percent/100) ** y
            dcf = pcf * df
            self._projected_cash_flow.append(pcf)
            self._discount_factor.append(df)
            self._discounted_cash_flow.append(dcf)

        self._net_present_value = self._sum(self._discounted_cash_flow)
        self._perpetuity_growth_rate_percent = self._gdp_growth_rate_percent
        self._last_year_discounted_cash_flow = self._discounted_cash_flow[len(self._discounted_cash_flow)-1]
        self._perpetuity_value = (self._last_year_discounted_cash_flow *
                                  (1+self._perpetuity_growth_rate_percent/100)) / \
                                 (self._discount_rate_percent/100-self._perpetuity_growth_rate_percent/100)
        self._last_year_discount_factor = self._discount_factor[len(self._discount_factor)-1]
        self._discounted_perpetuity_value = self._perpetuity_value * self._last_year_discount_factor

        self._intrinsic_value = self._net_present_value + self._discounted_perpetuity_value + self._total_business_cash - self._total_business_debt
        self._intrinsic_value_share = self._intrinsic_value / self._shares_outstanding

        self._proyections_df = pandas.DataFrame(
            {
                "Projected Cash Flow" : self._us_curr_list(self._projected_cash_flow),
                "Discount Factor" : self._discount_factor,
                "Discounted Cash Flow" : self._us_curr_list(self._discounted_cash_flow)
             }
        )

        print("###############################################################")
        print("#                       Intrinsic Value                       #")
        print("###############################################################")
        print("Initial Parameters")
        print("Company Name: "+self._company)
        print("Ticker: "+self._ticker)
        print("Date: "+str(self._date))
        print("Shares Outstanding: "+self._us_num(self._shares_outstanding))
        print("Free Cash Flow: "+self._us_curr(self._free_cash_flow))
        print("Business Grow Rate: "+str(self._business_grow_rate_percent)+"%")
        print("Business Tax Rate: "+str(self._business_tax_rate_percent)+"%")
        print("Business Interest Rate: "+str(self._business_interest_rate_percent)+"%")
        print("Market Capitalization: "+self._us_curr(self._market_capitalization))
        print("Beta Coefficient: "+str(self._beta_coefficient))
        print("Risk Free Rate: "+str(self._risk_free_rate_percent)+"%")
        print("Total Business Cash: "+self._us_curr(self._total_business_cash))
        print("----------------------------------------------------------------")
        print("Calculations")
        print("Market Value of Debt: "+self._us_curr(self._market_value_debt))
        print("Cost of Debt: "+str(self._cost_debt)+"%")
        print("Cost of Equity: "+str(self._cost_equity)+"%")
        print("Discount Rate: "+str(self._discount_rate_percent)+"%")
        print("Projections")
        print(self._proyections_df)
        print("Net Present Value: "+self._us_curr(self._net_present_value))
        print("Perpetuity Value: "+self._us_curr(self._perpetuity_value))
        print("Discounted Perpetuity Value: "+self._us_curr(self._discounted_perpetuity_value))
        print("Intrinsic Value: "+self._us_curr(self._intrinsic_value))
        print("Intrinsic Value per Share: "+self._us_curr(self._intrinsic_value_share))

    def _sum(self, values):
        sum = 0
        for v in values:
            sum += v
        return sum

    def _us_num(self, number):
        return babel.numbers.format_number(number, locale="en_US")

    def _us_curr(self, number):
        return babel.numbers.format_currency(number, "USD", locale="en_US")

    def _us_curr_list(self, values):
        us_curr_list = []
        for v in values:
            us_curr_list.append(self._us_curr(v))
        return us_curr_list
