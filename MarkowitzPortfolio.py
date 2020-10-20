# Builds a stock investment portfolio using the Markowitz theory.
# This script uses yahoo finance to retreive stock data.
# Expected return.
# 1.- Download a group of company stock prices from a given period.
# 2.- Calculate the differences.

import decimal, pandas, logging, matplotlib, yfinance, pprint, datetime

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
        return covar / decimal.Decimal.sqrt(variance_x * variance_y)

    def _stock_expected_return(self,probability_list, return_list):
        expected = decimal.Decimal(0)
        for i in range(len(return_list)):
            expected += probability_list[i] * return_list[i]
        return expected/len(return_list)

    def _stock_variance(self,probability_list, return_list):
        expected_return = self._stock_expected_return(probability_list,return_list)
        variance = decimal.Decimal(0)
        for i in range(len(probability_list)):
            variance += probability_list[i]*(return_list[i]-expected_return)**2
        return variance

    def _stock_stdev(self, probability_list, return_list):
        return self._stock_variance(probability_list, return_list).sqrt()

    def __init__(self):
        company_list = ["AM", "ANET", "BAC", "CSCO", "INTC", "MU"]
        start_date = "2018-01-01"
        today_date = datetime.datetime.today()
        end_date = str(today_date.year)+"-"+str(today_date.month)+"-"+str(today_date.day)

        #Retrieve Data from Yahoo finance. Last values are at the End.
        stock_price_dict = {}
        for i in company_list:
            data = yfinance.download(i, start_date, end_date)
            stock_price_dict[i] = data["Close"]

        with pandas.ExcelWriter("tempfiles\\MarkowitzPort.xlsx") as writer:
            for i in company_list:
                stock_price_dict[i].to_excel(writer, sheet_name=i)

        diferences_dict = {}
        expected_return_dict = {}
        variance_dict = {}
        stdev_dict = {}
        for i in company_list:
            diferences_list = []
            stock_prices = stock_price_dict[i]
            for j in range(len(stock_prices)):
                if j > 0:
                    diferences_list.append(stock_prices[j]/stock_prices[j-1]-1)
            diferences_dict[i] = diferences_list
            probability_list = [1/len(diferences_list)] * len(diferences_list)
            expected_return_dict[i] = self._stock_expected_return(probability_list, diferences_list)
            variance_dict[i] = self._stock_variance(probability_list,diferences_list)
            stdev_dict[i] = self._stock_stdev(probability_list,diferences_list)

        print("Expected Returns: ")
        pprint.pprint(expected_return_dict)
        print("Variance: ")
        pprint.pprint(variance_dict)
        print("Standard Deviation: ")
        pprint.pprint(stdev_dict)



        print("Markowitz Investment Portfolio Builder")
        print("Companies: ")
        pprint.pprint(company_list)
        print("Start Date:" + start_date)
        print("End Date: " + end_date)





        # Get the data for the stock Apple by specifying the stock ticker, start date, and end date
        #data = yfinance.download('AAPL', '2016-01-01', '2020-01-01')
        #print(data)
        # Plot the close prices
        #data["Close"].plot()
        #matplotlib.pyplot.show()

        #ticker_data = yfinance.Ticker("AAPL")
        #pprint.pprint(ticker_data.info)
        #print(ticker_data.calendar)



