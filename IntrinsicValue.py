import decimal, babel, datetime, pandas

class IntrinsicValueParameters:
    def __init__(self):
        # company: string
        self.company = None
        # ticker: string
        self.ticker = None
        # current_share_price: decimal.Decimal()
        self.current_share_price = None
        # date: datetime.datetime
        self.date = None
        # shares_outstanding: decimal.Decimal()
        self.shares_outstanding = None
        # free_cash_flow : decimal.Decimal()
        self.free_cash_flow = None
        # business_grow_rate_percent : decimal.Decimal()
        self.business_grow_rate_percent = None
        # business_tax_rate_percent : decimal.Decimal()
        self.business_tax_rate_percent = None
        # business_interest_rate_percent : decimal.Decimal()
        self.business_interest_rate_percent = None
        # market_capitalization : decimal.Decimal()
        self.market_capitalization = None
        # beta_coefficient : decimal.Decimal()
        self.beta_coefficient = None
        # risk_free_rate_percent : decimal.Decimal()
        self.risk_free_rate_percent = None
        # market_risk_premium_percent : decimal.Decimal()
        self.market_risk_premium_percent = None
        # long_term_debt : decimal.Decimal()
        self.long_term_debt = None
        # short_term_debt : decimal.Decimal()
        self.short_term_debt = None
        # total_business_cash : decimal.Decimal()
        self.total_business_cash = None
        # gdp_growth_rate_percent : decimal.Decimal()
        self.gdp_growth_rate_percent = None
        # total_business_debt : decimal.Decimal()
        self.total_business_debt = None

class IntrinsicValue:
    def __init__(self, params):
        self._company = params.company
        self._ticker = params.ticker
        self._current_share_price = params.current_share_price
        self._date = params.date
        self._shares_outstanding = params.shares_outstanding
        self._free_cash_flow = params.free_cash_flow
        self._business_grow_rate_percent = params.business_grow_rate_percent
        self._business_tax_rate_percent = params.business_tax_rate_percent
        self._business_interest_rate_percent = params.business_interest_rate_percent
        self._market_capitalization = params.market_capitalization
        self._beta_coefficient = params.beta_coefficient
        self._risk_free_rate_percent = params.risk_free_rate_percent
        self._market_risk_premium_percent = params.market_risk_premium_percent
        self._long_term_debt = params.long_term_debt
        self._short_term_debt = params.short_term_debt
        self._total_business_cash = params.total_business_cash
        self._gdp_growth_rate_percent = params.gdp_growth_rate_percent
        self._total_business_debt = params.total_business_debt

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

        self._net_present_value = sum(self._discounted_cash_flow)
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
        print("Current Share Price: "+self._us_curr(self._current_share_price))
        print("Date: "+str(self._date))
        print("Shares Outstanding: "+self._us_num(self._shares_outstanding))
        print("Free Cash Flow: "+self._us_curr(self._free_cash_flow))
        print("Business Grow Rate: "+str(self._business_grow_rate_percent)+"%")
        print("Business Tax Rate: "+str(self._business_tax_rate_percent)+"%")
        print("Business Interest Rate: "+str(self._business_interest_rate_percent)+"%")
        print("Market Capitalization: "+self._us_curr(self._market_capitalization))
        print("Beta Coefficient: "+str(self._beta_coefficient))
        print("Risk Free Rate: "+str(self._risk_free_rate_percent)+"%")
        print("Market Risk Premium: "+str(self._market_risk_premium_percent)+"%")
        print("Long Term Debt: "+self._us_curr(self._long_term_debt))
        print("Short Term Debt: "+self._us_curr(self._short_term_debt))
        print("Total Business Cash: "+self._us_curr(self._total_business_cash))
        print("GDP Growth Rate: "+str(self._gdp_growth_rate_percent)+"%")
        print("Total Business Debt: "+self._us_curr(self._total_business_debt))
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

    def _us_num(self, number):
        return babel.numbers.format_number(number, locale="en_US")

    def _us_curr(self, number):
        return babel.numbers.format_currency(number, "USD", locale="en_US")

    def _us_curr_list(self, values):
        us_curr_list = []
        for v in values:
            us_curr_list.append(self._us_curr(v))
        return us_curr_list


def main():
    #Cisco Systems
    # params = IntrinsicValueParameters()
    # params.company = "Cisco Systems"
    # params.ticker = "CSCO"
    # params.current_share_price = decimal.Decimal(39.81)
    # params.date = datetime.datetime.strptime("2020/10/14", "%Y/%m/%d")
    # params.shares_outstanding = decimal.Decimal("4233430000")
    # params.free_cash_flow = decimal.Decimal("14656000000")
    # params.business_grow_rate_percent = decimal.Decimal("1.55")
    # params.business_tax_rate_percent = decimal.Decimal("19.73")
    # params.business_interest_rate_percent = decimal.Decimal("3.10")
    # params.market_capitalization = decimal.Decimal("168533000000")
    # params.beta_coefficient = decimal.Decimal("0.83")
    # params.risk_free_rate_percent = decimal.Decimal("0.732")
    # params.market_risk_premium_percent = decimal.Decimal("5.6")
    # params.long_term_debt = decimal.Decimal("11578000000")
    # params.short_term_debt = decimal.Decimal("3005000000")
    # params.total_business_cash = decimal.Decimal("29419000000")
    # params.gdp_growth_rate_percent = decimal.Decimal("1.26")
    # params.total_business_debt = decimal.Decimal("17499600000")
    # intrinsic_value = IntrinsicValue(params)

    #Intel Corporation
    # params = IntrinsicValueParameters()
    # params.company = "Intel Corporation"
    # params.ticker = "INTC"
    # params.current_share_price = decimal.Decimal("53.90")
    # params.date = datetime.datetime.strptime("2020/10/22", "%Y/%m/%d")
    # params.shares_outstanding = decimal.Decimal("4250000000")
    # params.free_cash_flow = decimal.Decimal("21900000000")
    # params.business_grow_rate_percent = decimal.Decimal("5.99")
    # params.business_tax_rate_percent = decimal.Decimal("15.20")
    # params.business_interest_rate_percent = decimal.Decimal("1.90")
    # params.market_capitalization = decimal.Decimal("229237000000")
    # params.beta_coefficient = decimal.Decimal("0.72")
    # params.risk_free_rate_percent = decimal.Decimal("0.732")
    # params.market_risk_premium_percent = decimal.Decimal("5.6")
    # params.long_term_debt = decimal.Decimal("36059000000")
    # params.short_term_debt = decimal.Decimal("504000000")
    # params.total_business_cash = decimal.Decimal("25820000000")
    # params.gdp_growth_rate_percent = decimal.Decimal("1.26")
    # params.total_business_debt = decimal.Decimal("38350000000")
    # intrinsic_value = IntrinsicValue(params)

    #Advanced Micro Devices, Inc.
    params = IntrinsicValueParameters()
    params.company = "Advanced Micro Devices, Inc."
    params.ticker = "AMD"
    params.current_share_price = decimal.Decimal("78.88")
    params.date = datetime.datetime.strptime("2020/10/27", "%Y/%m/%d")
    params.shares_outstanding = decimal.Decimal("1170000000")
    params.free_cash_flow = decimal.Decimal("610000000")
    params.business_grow_rate_percent = decimal.Decimal("1.65")
    params.business_tax_rate_percent = decimal.Decimal("8.33")
    params.business_interest_rate_percent = decimal.Decimal("7.03")
    params.market_capitalization = decimal.Decimal("93240000000")
    params.beta_coefficient = decimal.Decimal("2.29")
    params.risk_free_rate_percent = decimal.Decimal("0.732")
    params.market_risk_premium_percent = decimal.Decimal("5.6")
    params.long_term_debt = decimal.Decimal("486000000")
    params.short_term_debt = decimal.Decimal("0")
    params.total_business_cash = decimal.Decimal("1780000000")
    params.gdp_growth_rate_percent = decimal.Decimal("1.26")
    params.total_business_debt = decimal.Decimal("894000000")
    intrinsic_value = IntrinsicValue(params)



