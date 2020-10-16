# Builds a stock investment portfolio using the Markowitz theory.
# This script uses yahoo finance to retreive stock data.
# Expected return.
# 1.- Download a group of company stock prices from a given period.
# 2.- Calculate the differences.

import decimal, pandas, logging, matplotlib, yfinance, pprint

class MarkowitzPortofolio:

    def _range(self, min, max):
        return max - min

    def _mean(self, number_list):
        mean = decimal.Decimal(0)
        for i in number_list:
            mean += i
        return mean / len(number_list)

    def _variance(self, number_list):
        mean = self._mean(number_list)
        variance = decimal.Decimal(0)
        for i in number_list:
            variance += (mean - i)**2
        return variance / len(number_list)

    def _stdev(self, number_list):
        return decimal.Decimal.sqrt(self._variance(number_list))

    def _covar(self, number_list_x, number_list_y):
        covar = decimal.Decimal(0)
        mean_x = self._mean(number_list_x)
        mean_y = self._mean(number_list_y)
        n = len(number_list_x)
        for i in range(n):
            covar += (number_list_x[i]-mean_x) * (number_list_y[i]-mean_y)
        return covar / n

    def _correl(self, number_list_x, number_list_y):
        covar = self._covar(number_list_x,number_list_y)
        variance_x = self._variance(number_list_x)
        variance_y = self._variance(number_list_y)
        return  covar / decimal.Decimal.sqrt(variance_x * variance_y)

    def _expected_return(self,probability_list, return_list):
        expected = decimal.Decimal(0)
        for i in range(len(return_list)):
            expected += probability_list[i] * return_list[i]
        return expected

    def __init__(self):

        portfolio_list = ["AAPL"]



        # Get the data for the stock Apple by specifying the stock ticker, start date, and end date
        data = yfinance.download('AAPL', '2016-01-01', '2020-01-01')
        print(data)
        # Plot the close prices
        #data["Close"].plot()
        #matplotlib.pyplot.show()

        ticker_data = yfinance.Ticker("AAPL")
        pprint.pprint(ticker_data.info)


        print(ticker_data.calendar)



