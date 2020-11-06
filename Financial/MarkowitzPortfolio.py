# Builds a stock investment portfolio using the Markowitz theory.
# This script uses yahoo finance to retreive stock data.
# Expected return.
# 1.- Download a group of company stock prices from a given period.
# 2.- Calculate the differences.

import pandas, logging, matplotlib, yfinance, pprint, datetime, os, numpy, scipy.optimize, math

class MarkowitzPortofolio:

    def _range(self, min, max):
        return max - min

    def _mean(self, number_list):
        return sum(number_list) / len(number_list)

    def _variance(self, number_list):
        mean = self._mean(number_list)
        variance = 0
        for i in number_list:
            variance += (mean - i)**2
        return variance / len(number_list)

    def _stdev(self, number_list):
        return math.sqrt(self._variance(number_list))

    def _variation_coeficient(self, number_list):
        return self._stdev(number_list) / self._mean(number_list)

    def _covar(self, number_list_x, number_list_y):
        #logging.debug("number_list_x: "+str(number_list_x))
        #logging.debug("number_list_y: "+str(number_list_y))
        covar = 0
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
        return covar / math.sqrt(variance_x * variance_y)

    def _sumprod(self, number_list_x, number_list_y):
        sum = 0
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
        variance = 0
        for i in range(len(probability_list)):
            variance += probability_list[i]*(diferences_list[i]-expected_return_mean)**2
        return variance

    def _stock_stdev(self, probability_list, diference_list):
        return math.sqrt(self._stock_variance(probability_list, diference_list))

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
                correl = self._correl(expected_return_dict[i], expected_return_dict[j])
                matrix_row.append(correl)
            matrix.append(matrix_row)
        return matrix

    def _portfolio_return(self, inv_distribution_list):
        return self._sumprod(self._expected_return_mean_list, inv_distribution_list)

    def _portfolio_risk(self, inv_distribution_list):
        risk = 0
        for i in range(len(self._covar_matrix)):
            for j in range(len(self._covar_matrix)):
                risk += inv_distribution_list[i]*inv_distribution_list[j]*self._covar_matrix[i][j]
        return math.sqrt(risk)

    def _objective_maximize_return(self, inv_distribution_list):
        return -self._portfolio_return(inv_distribution_list)

    def _objective_minimize_risk(self,inv_distribution_list):
        return self._portfolio_risk(inv_distribution_list)

    def _constrain1(self, inv_distribution_list):
        return sum(inv_distribution_list) - 1.0

    def _load_from_yahoo(self,company_list, file_name, start_date, end_date):
        stock_price_dict = {}
        for i in company_list:
            data = yfinance.download(i, start_date, end_date)
            stock_price_dict[i] = data["Close"]

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
                stock_price_dict[i] = stock_df[i]
            else:
                first = False
        return stock_price_dict

    def _matrix_to_dataframe(self,columns, matrix):
        dictionary = {}
        for i in range(len(matrix)):
            dictionary[columns[i]] = matrix[i]
        return pandas.DataFrame(dictionary,index=columns)

    def __init__(self):
        # Define the Filename of Data Source
        FILE_NAME = "../tempfiles/MarkowitzPort.xlsx"

        # Define the comapnies which will be included in the analysis.
        self._company_list = ["AM", "ANET", "BAC", "CSCO", "INTC", "MU"]

        # Define the period to extract the stock price values.
        start_date = "2018-01-01"
        today_date = datetime.datetime.today()
        end_date = str(today_date.year)+"-"+str(today_date.month)+"-"+str(today_date.day)

        # Retrieve Data from File, is an error is present, retrieve from Yahoo finance.
        # Most recent values are at the End.
        stock_price_dict = self._load_from_file(self._company_list,FILE_NAME,start_date,end_date)
        if stock_price_dict is None:
            stock_price_dict = self._load_from_yahoo(self._company_list,FILE_NAME,start_date,end_date)


        diferences_dict = {}
        self._expected_return_mean_dict = {}
        self._expected_return_mean_list = []
        self._inv_distribution_list = [1/len(self._company_list)] * len(self._company_list)
        self._expected_return_dict = {}
        self._variance_dict = {}
        self._stdev_dict = {}
        self._variation_coeficient_dict = {}
        self._performance_dict = {}
        self._statistics_dict = {}

        statistics_rows = ["Expected Return", "Variance", "Standard Deviation", "Variation Coeficient", "Performance"]
        for i in self._company_list:
            diferences_list = []
            stock_prices = stock_price_dict[i]
            for j in range(len(stock_prices)):
                if j > 0:
                    diferences_list.append(stock_prices[j]/stock_prices[j-1]-1)

            probability_list = [1/len(diferences_list)] * len(diferences_list)
            expected_return_list = self._stock_expected_return(probability_list, diferences_list)
            expected_return_mean = self._mean(expected_return_list)
            variance = self._stock_variance(probability_list, diferences_list)
            stdev = self._stock_stdev(probability_list, diferences_list)
            variation_coef = self._stock_variation_coef(probability_list, diferences_list)
            performance = self._stock_perfomance(probability_list, diferences_list)
            diferences_dict[i] = diferences_list
            self._expected_return_dict[i] = expected_return_list
            self._expected_return_mean_dict[i] = expected_return_mean
            self._expected_return_mean_list.append(expected_return_mean)
            self._variance_dict[i] = variance
            self._stdev_dict[i] = stdev
            self._variation_coeficient_dict[i] = variation_coef
            self._performance_dict[i] = performance
            self._statistics_dict[i] = [expected_return_mean, variance, stdev, variation_coef, performance]
            #logging.debug("diferences_dict[i]: "+str(diferences_dict[i]))
            #logging.debug("probability_list: "+str(probability_list))
            #logging.debug("expected_return_dict[i]: "+str(expected_return_dict[i]))
            #logging.debug("type probability_list[0]: "+str(type(probability_list[0])))
            #logging.debug("type diferences_list[0]: "+str(type(diferences_list[0])))

        self._covar_matrix = self._covariance_matrix(self._company_list, self._expected_return_dict)
        self._correl_matrix = self._correlation_matrix(self._company_list, self._expected_return_dict)

        # Maximize Porfolio Return.
        method = "Powell"
        b = (0.0, 1.0)
        bounds = [b] * len(self._company_list)
        x0 = numpy.array(self._inv_distribution_list)
        cons1 = {"type": "eq", "fun": "self._constrain1"}
        constraints = [cons1]
        solution_max_return = scipy.optimize.minimize(
            fun=self._objective_maximize_return,
            method=method,
            x0=x0,
            bounds=bounds,
            constraints=constraints
        )

        # Minimize Portfolio Risk.
        method = "Powell"
        b = (0.0, 1.0)
        bounds = [b] * len(self._company_list)
        x0 = numpy.array(self._inv_distribution_list)
        cons1 = {"type": "eq", "fun": "self._constrain1"}
        constraints = [cons1]
        solution_min_risk = scipy.optimize.minimize(
            fun=self._objective_minimize_risk,
            method=method,
            x0 = x0,
            bounds= bounds,
            constraints=constraints
        )

        print("Markowitz Investment Portfolio Builder")
        print("Companies: ")
        pprint.pprint(self._company_list)
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
        statistics_df = pandas.DataFrame(self._statistics_dict, statistics_rows)
        print(statistics_df)

        print("\nCovariance Matrix")
        covariance_matrix_df = self._matrix_to_dataframe(self._company_list, self._covar_matrix)
        print(covariance_matrix_df)
        print("\nCorrelation Matrix")
        correlation_matrix_df = self._matrix_to_dataframe(self._company_list, self._correl_matrix)
        print(correlation_matrix_df)

        print("----------------------------------------------------------------")
        print("Suboptimal Solution")
        print("Investment Distribution List: ")
        print(str(self._inv_distribution_list))
        print("Porfolio Return: "+str(self._portfolio_return(self._inv_distribution_list)))
        print("Portfolio Risk: "+str(self._portfolio_risk(self._inv_distribution_list)))
        print("----------------------------------------------------------------")
        print("Optimization Maximize Portfolio Return")
        print("Method: "+method)
        print(solution_max_return)
        print("----------------------------------------------------------------")
        print("Maximization Optimal Solution")
        print(solution_max_return.x)
        print("Portfolio Return: "+str(self._portfolio_return(solution_max_return.x)))
        print("Portfolio Risk: "+str(self._portfolio_risk(solution_max_return.x)))
        print("----------------------------------------------------------------")
        print("----------------------------------------------------------------")
        print("Optimization Maximize Portfolio Risk")
        print("Method: "+method)
        print(solution_min_risk)
        print("----------------------------------------------------------------")
        print("Minimization Optimal Solution")
        print(solution_min_risk)
        print("----------------------------------------------------------------")
        print(solution_min_risk.x)
        print("Portfolio Return: "+str(self._portfolio_return(solution_min_risk.x)))
        print("Portfolio Risk: "+str(self._portfolio_risk(solution_min_risk.x)))


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

def main():
    mp = MarkowitzPortofolio()

if __name__ == "__main__":
    main()