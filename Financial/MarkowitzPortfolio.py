# Builds a stock investment portfolio using the Markowitz theory.
# This script uses yahoo finance to retreive stock data.
# Expected return.
# 1.- Download a group of company stock prices from a given period.
# 2.- Calculate the differences.

import decimal, pandas, logging, matplotlib, yfinance, pprint, datetime, os

class MarkowitzPortofolio:

    def _range(self, min, max):
        return max - min

    def _mean(self, number_list):
        return sum(number_list) / len(number_list)

    def _variance(self, number_list):
        mean = self._mean(number_list)
        variance = decimal.Decimal(0)
        for i in number_list:
            variance += (mean - i)**2
        return variance / len(number_list)

    def _stdev(self, number_list):
        return decimal.Decimal.sqrt(self._variance(number_list))

    def _variation_coeficient(self, number_list):
        return self._stdev(number_list) / self._mean(number_list)

    def _covar(self, number_list_x, number_list_y):
        #logging.debug("number_list_x: "+str(number_list_x))
        #logging.debug("number_list_y: "+str(number_list_y))
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

    def _sumprod(self, number_list_x, number_list_y):
        sum = decimal.Decimal(0)
        for i in range(len(number_list_x)):
            sum += number_list_x[i] * number_list_y[i]
        return sum

    def _stock_expected_return(self, probability_list, diferences_list):
        expected_return_list = []
        for i in range(len(diferences_list)):
            expected_return_list.append(probability_list[i] * diferences_list[i])
        return expected_return_list

    def _stock_variance(self, probability_list, diferences_list):
        expected_return_list = self._stock_expected_return(probability_list,diferences_list)
        expected_return_mean = self._mean(expected_return_list)
        variance = decimal.Decimal(0)
        for i in range(len(probability_list)):
            variance += probability_list[i]*(diferences_list[i]-expected_return_mean)**2
        return variance

    def _stock_stdev(self, probability_list, diference_list):
        return self._stock_variance(probability_list, diference_list).sqrt()

    def _stock_variation_coef(self, probability_list, diference_list):
        return self._stock_stdev(probability_list, diference_list) / \
               self._mean(self._stock_expected_return(probability_list, diference_list))

    def _stock_perfomance(self, probability_list, diference_list):
        return self._mean(self._stock_expected_return(probability_list, diference_list)) / \
               self._stock_stdev(probability_list, diference_list)


    def _covariance_matrix(self, company_list, expected_return_dict):
        matrix = []
        for i in company_list:
            matrix_row = []
            for j in company_list:
                covar = self._covar(expected_return_dict[i], expected_return_dict[j])
                matrix_row.append(covar)
            matrix.append(matrix_row)
        return matrix

    def _correlation_matrix(self, company_list, expected_return_dict):
        matrix = []
        for i in company_list:
            matrix_row = []
            for j in company_list:
                correl = self._correl(expected_return_dict[i],expected_return_dict[j])
                matrix_row.append(correl)
            matrix.append(matrix_row)
        return matrix

    def _portfolio_return(self, expected_return_mean_list, inv_prop_list):
        return self._sumprod(expected_return_mean_list, inv_prop_list)

    def _porfolio_risk(self,covariance_matrix, inv_prop_list):
        risk = decimal.Decimal(0)
        for i in range(len(covariance_matrix)):
            for j in range(len(covariance_matrix)):
                risk += inv_prop_list[i]*inv_prop_list[j]*covariance_matrix[i][j]
        return risk.sqrt()


    def _load_from_yahoo(self,company_list, file_name, start_date, end_date):
        stock_price_dict = {}
        for i in company_list:
            data = yfinance.download(i, start_date, end_date)
            stock_price_dict[i] = data["Close"].apply(decimal.Decimal)

        stock_df = pandas.DataFrame(stock_price_dict)

        with pandas.ExcelWriter(FILE_NAME) as writer:
            stock_df.to_excel(writer,sheet_name="Stock Prices")

        return stock_price_dict

    def _load_from_file(self,company_list, file_name, start_date, end_date):
        stock_df = pandas.read_excel(file_name)
        stock_price_dict = {}
        first = True
        for i in stock_df.columns:
            if first is False:
                stock_price_dict[i] = stock_df[i].apply(decimal.Decimal)
            else:
                first = False
        return stock_price_dict

    def _matrix_to_dataframe(self,columns, matrix):
        dictionary = {}
        for i in range(len(matrix)):
            dictionary[columns[i]] = matrix[i]
        return pandas.DataFrame(dictionary,index=columns)



    def __init__(self):
        #Define the Filename of Data Source
        FILE_NAME = "../tempfiles/MarkowitzPort.xlsx"
        #Define the comapnies which will be included in the analysis.
        company_list = ["AM", "ANET", "BAC", "CSCO", "INTC", "MU"]
        #Define the period to extract the stock price values.
        start_date = "2018-01-01"
        today_date = datetime.datetime.today()
        end_date = str(today_date.year)+"-"+str(today_date.month)+"-"+str(today_date.day)

        #Retrieve Data from File, is an error is present, retrieve from Yahoo finance.
        #Most recent values are at the End.
        stock_price_dict = self._load_from_file(company_list,FILE_NAME,start_date,end_date)
        if stock_price_dict is None:
            stock_price_dict = self._load_from_yahoo(company_list,FILE_NAME,start_date,end_date)


        diferences_dict = {}
        expected_return_mean_dict = {}
        expected_return_dict = {}
        variance_dict = {}
        stdev_dict = {}
        variation_coeficient_dict = {}
        performance_dict = {}
        statistics_dict = {}
        statistics_rows = ["Expected Return","Variance","Standard Deviation","Variation Coeficient","Performance"]
        for i in company_list:
            diferences_list = []
            stock_prices = stock_price_dict[i]
            for j in range(len(stock_prices)):
                if j > 0:
                    diferences_list.append(stock_prices[j]/stock_prices[j-1]-1)

            probability_list = [decimal.Decimal(1/len(diferences_list))] * len(diferences_list)
            expected_return_list = self._stock_expected_return(probability_list, diferences_list)
            expected_return = self._mean(expected_return_list)
            variance = self._stock_variance(probability_list, diferences_list)
            stdev = self._stock_stdev(probability_list, diferences_list)
            variation_coef = self._stock_variation_coef(probability_list, diferences_list)
            performance = self._stock_perfomance(probability_list, diferences_list)
            diferences_dict[i] = diferences_list
            expected_return_dict[i] = expected_return_list
            expected_return_mean_dict[i] = expected_return
            variance_dict[i] = variance
            stdev_dict[i] = stdev
            variation_coeficient_dict[i] = variation_coef
            performance_dict[i] = performance
            statistics_dict[i] = [expected_return,variance,stdev,variation_coef,performance]
            #logging.debug("diferences_dict[i]: "+str(diferences_dict[i]))
            #logging.debug("probability_list: "+str(probability_list))
            #logging.debug("expected_return_dict[i]: "+str(expected_return_dict[i]))
            #logging.debug("type probability_list[0]: "+str(type(probability_list[0])))
            #logging.debug("type diferences_list[0]: "+str(type(diferences_list[0])))

        covar_matrix = self._covariance_matrix(company_list, expected_return_dict)
        correl_matrix = self._correlation_matrix(company_list, expected_return_dict)


        print("Markowitz Investment Portfolio Builder")
        print("Companies: ")
        pprint.pprint(company_list)
        print("Start Date:" + start_date)
        print("End Date: " + end_date)

        # print("\nExpected Returns: ")
        # pprint.pprint(expected_return_mean_dict)
        # print("\nVariance: ")
        # pprint.pprint(variance_dict)
        # print("\nStandard Deviation: ")
        # pprint.pprint(stdev_dict)
        # print("\nVariation Coeficient")
        # pprint.pprint(variation_coeficient_dict)
        # print("\nPerformance")
        # pprint.pprint(performance_dict)

        print("\nStatistics")
        statistics_df = pandas.DataFrame(statistics_dict,statistics_rows)
        print(statistics_df)

        print("\nCovariance Matrix")
        covariance_matrix_df = self._matrix_to_dataframe(company_list, covar_matrix)
        print(covariance_matrix_df)
        print("\nCorrelation Matrix")
        correlation_matrix_df = self._matrix_to_dataframe(company_list, correl_matrix)
        print(correlation_matrix_df)

        SAVE_FILE_NAME = "../tempfiles/MarkowitzPortResults.xlsx"
        with pandas.ExcelWriter(SAVE_FILE_NAME) as writer:
            pandas.DataFrame(stock_price_dict).astype("float64").to_excel(writer, sheet_name="Stock Prices")
            statistics_df.astype("float64").to_excel(writer, sheet_name="Statistics")
            covariance_matrix_df.astype("float64").to_excel(writer, sheet_name="Covariance Matrix")
            correlation_matrix_df.astype("float64").to_excel(writer, sheet_name="Correlation Matrix")




        # Get the data for the stock Apple by specifying the stock ticker, start date, and end date
        #data = yfinance.download('AAPL', '2016-01-01', '2020-01-01')
        #print(data)
        # Plot the close prices
        #data["Close"].plot()
        #matplotlib.pyplot.show()

        #ticker_data = yfinance.Ticker("AAPL")
        #pprint.pprint(ticker_data.info)
        #print(ticker_data.calendar)
