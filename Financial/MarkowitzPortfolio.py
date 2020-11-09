# Builds a stock investment portfolio using the Markowitz theory.
# This script uses yahoo finance to retreive stock data.
# Expected return.
# 1.- Download a group of company stock prices from a given period.
# 2.- Calculate the differences.

# Get the data for the stock Apple by specifying the stock ticker, start date, and end date
# data = yfinance.download('AAPL', '2016-01-01', '2020-01-01')
# print(data)
# Plot the close prices
# data["Close"].plot()
# matplotlib.pyplot.show()

# ticker_data = yfinance.Ticker("AAPL")
# pp(ticker_data.info)
# print(ticker_data.calendar)


import pandas, logging, matplotlib.pyplot as plt, yfinance
import datetime, os, numpy, scipy.optimize, math, random
from pprint import pprint as pp


class GeneticIndividual:

    @staticmethod
    def random_list(gene_size, bounds):
        x = [random.uniform(bounds[i][0], bounds[i][1]) for i in range(gene_size)]
        s = sum(x)
        x = [i/s for i in x]
        return x


    @staticmethod
    def random_individual(gene_size, minimize_fitness_function, bounds):
        x = GeneticIndividual.random_list(gene_size=gene_size, bounds=bounds)
        return GeneticIndividual(
            minimize_fitness_function=minimize_fitness_function,
            x=x,
            bounds=bounds,
        )

    @staticmethod
    def normalize_values(x):
        s = sum(x)
        n = len(x)
        if s > 1.0:
            d = [(s - 1.0)/n] * n
            x1 = [x[i]-d[i] for i in range(n)]
        elif s < 1.0:
            d = [(1.0 - s)/n] * n
            x1 = [x[i]+d[i] for i in range(n)]
        return x1

    @staticmethod
    def recombine(individual1, individual2):
        x1 = individual1.x
        x2 = individual2.x
        x3 = [0] * len(x1)
        for i in range(len(x1)):
            x3[i] = (x1[i] + x2[i])/2

        return GeneticIndividual(
            minimize_fitness_function=individual1.minimize_fitness_function,
            x=x3,
            bounds=individual1.bounds,
            )

    def mutate1(self):
        n = len(self.x)
        while True:
            i = random.randint(0, n - 1)
            j = random.randint(0, n - 1)
            if i != j:
                break
        self.x[i], self.x[j] = self.x[j], self.x[i]

    def mutate2(self):
        n = len(self.x)
        while True:
            i = random.randint(0, n - 1)
            j = random.randint(0, n - 1)
            if i != j:
                break
        y = self.x[i] + self.x[j]
        r = random.random()
        self.x[i] = y*r
        self.x[j] = y*(1-r)

    def mutate3(self):
        self.x = GeneticIndividual.random_list(gene_size=self.x, bounds=self.bounds)



    def __init__(self, minimize_fitness_function, x, bounds):
        self.minimize_fitness_function= minimize_fitness_function
        self.x = x
        self.bounds = bounds

    def fitness(self):
        return self.minimize_fitness_function(self.x)

    def __str__(self):
        string = str(self.x) + "\t" + str(sum(self.x))+"\t"+str(self.fitness())
        return string

class Population:
    @staticmethod
    def generate_population(
            minimize_fitness_function,
            x0,
            bounds,
            population_size
            ):
        first = GeneticIndividual(
            minimize_fitness_function=minimize_fitness_function,
            x=x0,
            bounds=bounds,
        )
        members = [first]
        if population_size > 1:
            for i in range(1, population_size):
                members.append(
                    GeneticIndividual.random_individual(
                        gene_size= len(x0),
                        minimize_fitness_function=minimize_fitness_function,
                        bounds=bounds,
                    )
                )
        return Population(members)

    @staticmethod
    def partition(arr, low, high):
        print("\n"+str(arr)+" low: "+str(low)+" high: "+str(high))
        i = (low - 1)  # index of smaller element
        pivot = arr[high].fitness()  # pivot

        for j in range(low, high):

            # If current element is smaller than or
            # equal to pivot
            if arr[j].fitness() <= pivot:
                # increment index of smaller element
                i = i + 1
                arr[i], arr[j] = arr[j], arr[i]

        arr[i+1], arr[high] = arr[high], arr[i + 1]
        return i+1

    @staticmethod
    def quickSort(arr, low, high):
        if len(arr) == 1:
            return arr
        if low < high:
            # pi is partitioning index, arr[p] is now
            # at right place
            pi = Population.partition(arr, low, high)

            # Separately sort elements before
            # partition and after partition
            Population.quickSort(arr, low, pi - 1)
            Population.quickSort(arr, pi + 1, high)
            return arr

    def __init__(self, members):
        self.members = members
        self.sort()

    def sort(self):
        self.members = Population.quickSort(self.members, 0, len(self.members)-1)



    def __str__(self):
        string = "----------------------------------------"
        string = "No\tGenetic Code\tFitness\n"
        string += "----------------------------------------"
        for i in self.members:
            string += "\n"+str(i)
        return string


class GeneticAlgorithm:
    #Genetic Algoritm Procedure
    #1 - Produce a population of size n, one individual with the initial values
    #    and the rest with random values.
    #2 -

    def __init__(self,
                 minimize_fitness_function, # Callable function
                 x0, # List of initial values
                 bounds, # List of tuple
                 population_size, # Integer values from 1 to n
                 mutation_rate, # Float values from 0 to 1
                 max_iterations # Integer values from 1 to n
                 ):

        self.minimize_fitness_function = minimize_fitness_function,
        self.x0 = x0,
        self.bounds = bounds
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.max_iterations = max_iterations
        self.params_dict = {
            "minimize_fitness_function": minimize_fitness_function,
            "x0": x0,
            "population_size": population_size,
            "mutation_rate": mutation_rate,
            "max_iterations": max_iterations
        }
        pp(self.params_dict)
        self.population = Population.generate_population(
             minimize_fitness_function=minimize_fitness_function,
             x0=x0,
             bounds=bounds,
             population_size=population_size
        )
        print(self.population)

    @staticmethod
    def test():
        gene_size = 5
        population_size = 20
        bounds = [(0.0, 1.0), (0.0, 1.0), (0.0, 1.0), (0.0, 1.0), (0.0, 1.0)]
        constraints = [{"type": "eq", "fun": MarkowitzPortofolio.constrain1}]
        rl = GeneticIndividual.random_list(gene_size=gene_size, bounds=bounds)
        print("Random List: "+str(rl))

        print("Create Single Individual")
        gi1 = GeneticIndividual(
            x=rl,
            minimize_fitness_function=fitness,
            bounds=bounds
        )
        print(gi1)
        print("Create Random Individual")
        gi1 = GeneticIndividual.random_individual(
            gene_size=gene_size,
            minimize_fitness_function=fitness,
            bounds=bounds
        )
        print(gi1)
        gi2 = GeneticIndividual.random_individual(
            gene_size=gene_size,
            minimize_fitness_function=fitness,
            bounds=bounds
        )
        print(gi2)
        print("\nCreate Population")
        pop = Population.generate_population(minimize_fitness_function=fitness, x0=rl, bounds=bounds, population_size=population_size)
        print(pop)
        print("---------------------------------------------------------")
        print("Mutation: ")
        print(gi1)
        print("---------------------")
        for i in range(100):
            gi1.mutate1()
            print(gi1)
        print("---------------------------------------------------------")
        print("\nRecombine:")
        print(gi1)
        print(gi2)
        g3 = GeneticIndividual.recombine(gi1, gi2)
        print(g3)




class MarkowitzPortofolio:

##############################################################
# Data Management

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




##############################################################
# Statistic Operations

    @staticmethod
    def range(min, max):
        return max - min

    @staticmethod
    def mean(number_list):
        return sum(number_list) / len(number_list)

    @staticmethod
    def variance(number_list):
        mean = MarkowitzPortofolio.mean(number_list)
        variance = 0
        for i in number_list:
            variance += (mean - i)**2
        return variance / len(number_list)

    @staticmethod
    def stdev(number_list):
        return math.sqrt(MarkowitzPortofolio.variance(number_list))

    @staticmethod
    def variation_coeficient(self, number_list):
        return MarkowitzPortofolio.stdev(number_list) / MarkowitzPortofolio.mean(number_list)

    @staticmethod
    def covar(number_list_x, number_list_y):
        #logging.debug("number_list_x: "+str(number_list_x))
        #logging.debug("number_list_y: "+str(number_list_y))
        covar = 0
        mean_x = MarkowitzPortofolio.mean(number_list_x)
        mean_y = MarkowitzPortofolio.mean(number_list_y)
        n = len(number_list_x)
        for i in range(n):
            covar += (number_list_x[i]-mean_x) * (number_list_y[i]-mean_y)
        return covar / n

    @staticmethod
    def correl(number_list_x, number_list_y):
        covar = MarkowitzPortofolio.covar(number_list_x, number_list_y)
        variance_x = MarkowitzPortofolio.variance(number_list_x)
        variance_y = MarkowitzPortofolio.variance(number_list_y)
        return covar / math.sqrt(variance_x * variance_y)

    @staticmethod
    def sumprod(number_list_x, number_list_y):
        sum = 0
        for i in range(len(number_list_x)):
            sum += number_list_x[i] * number_list_y[i]
        return sum

    @staticmethod
    def stock_expected_return(probability_list, diferences_list):
        expected_return_list = []
        for i in range(len(diferences_list)):
            expected_return_list.append(probability_list[i] * diferences_list[i]*365*100)
        return expected_return_list

    @staticmethod
    def stock_variance(probability_list, diferences_list):
        expected_return_list = MarkowitzPortofolio.stock_expected_return(probability_list, diferences_list)
        expected_return_mean = MarkowitzPortofolio.mean(expected_return_list)
        variance = 0
        for i in range(len(probability_list)):
            variance += probability_list[i]*(diferences_list[i]-expected_return_mean)**2
        return variance

    @staticmethod
    def stock_stdev(probability_list, diference_list):
        return math.sqrt(MarkowitzPortofolio.stock_variance(probability_list, diference_list))

    @staticmethod
    def stock_variation_coef(probability_list, diference_list):
        return MarkowitzPortofolio.stock_stdev(probability_list, diference_list) / \
               MarkowitzPortofolio.mean(MarkowitzPortofolio.stock_expected_return(probability_list, diference_list))

    @staticmethod
    def stock_perfomance(probability_list, diference_list):
        return MarkowitzPortofolio.mean(MarkowitzPortofolio.stock_expected_return(probability_list, diference_list)) / \
               MarkowitzPortofolio.stock_stdev(probability_list, diference_list)


    @staticmethod
    def covariance_matrix(company_list, expected_return_dict):
        matrix = []
        for i in company_list:
            matrix_row = []
            for j in company_list:
                covar = MarkowitzPortofolio.covar(expected_return_dict[i], expected_return_dict[j])
                matrix_row.append(covar)
            matrix.append(matrix_row)
        return matrix

    @staticmethod
    def correlation_matrix(company_list, expected_return_dict):
        matrix = []
        for i in company_list:
            matrix_row = []
            for j in company_list:
                correl = MarkowitzPortofolio.correl(expected_return_dict[i], expected_return_dict[j])
                matrix_row.append(correl)
            matrix.append(matrix_row)
        return matrix

    def _portfolio_return(self, inv_distribution_list):
        return MarkowitzPortofolio.sumprod(self._expected_return_mean_list, inv_distribution_list)

    def _portfolio_risk(self, inv_distribution_list):
        risk = 0
        for i in range(len(self._covar_matrix)):
            for j in range(len(self._covar_matrix)):
                risk += inv_distribution_list[i]*inv_distribution_list[j]*self._covar_matrix[i][j]
        return math.sqrt(risk)

##############################################################
# Optimization Operations
    def objective_maximize_return(self, inv_distribution_list):
        return -self._portfolio_return(inv_distribution_list)

    def objective_minimize_risk(self, inv_distribution_list):
        return self._portfolio_risk(inv_distribution_list)

    def objective_maximize_return_minimize_risk(self, inv_distribution_list):
        return -self._portfolio_return(inv_distribution_list) / self._portfolio_risk(inv_distribution_list)

    def constrain1(self, inv_distribution_list):
        return sum(inv_distribution_list) - 1.0


##############################################################
# Init

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
            expected_return_list = self.stock_expected_return(probability_list=probability_list, diferences_list=diferences_list)
            expected_return_mean = MarkowitzPortofolio.mean(number_list=expected_return_list)
            variance = MarkowitzPortofolio.stock_variance(probability_list=probability_list, diferences_list=diferences_list)
            stdev = MarkowitzPortofolio.stock_stdev(probability_list=probability_list, diference_list=diferences_list)
            variation_coef = MarkowitzPortofolio.stock_variation_coef(probability_list=probability_list, diference_list=diferences_list)
            performance = MarkowitzPortofolio.stock_perfomance(probability_list=probability_list, diference_list=diferences_list)
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

        self._covar_matrix = MarkowitzPortofolio.covariance_matrix(self._company_list, self._expected_return_dict)
        self._correl_matrix = MarkowitzPortofolio.correlation_matrix(self._company_list, self._expected_return_dict)

        method = "SLSQP"
        b = (0.0, 1.0)
        bounds = [b] * len(self._company_list)
        x0 = numpy.array(self._inv_distribution_list)
        cons1 = {"type": "eq", "fun": self.constrain1}
        constraints = [cons1]
        # Maximize Porfolio Return.
        solution_max_return = scipy.optimize.minimize(
            fun=self.objective_maximize_return,
            method=method,
            x0=x0,
            bounds=bounds,
            constraints=cons1
        )
        # Minimize Portfolio Risk.
        solution_min_risk = scipy.optimize.minimize(
            fun=self.objective_minimize_risk,
            method=method,
            x0=x0,
            bounds=bounds,
            constraints=cons1
        )
        # Maximize Portfolio Return considering Risk
        solution_max_return_min_risk = scipy.optimize.minimize(
            fun=self.objective_maximize_return_minimize_risk,
            method=method,
            x0=x0,
            bounds=bounds,
            constraints=cons1
        )

        print("Markowitz Investment Portfolio Builder")
        print("Companies: ")
        pp(self._company_list)
        print("Start Date:" + start_date)
        print("End Date: " + end_date)

        # print("\nExpected Returns: ")
        # pp(expected_return_mean_dict)
        # print("\nVariance: ")
        # pp(variance_dict)
        # print("\nStandard Deviation: ")
        # pp(stdev_dict)
        # print("\nVariation Coeficient")
        # pp(variation_coeficient_dict)
        # print("\nPerformance")
        # pp(performance_dict)

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
        print(str(self._inv_distribution_list)+"= "+str(sum(solution_max_return.x)))
        print("Porfolio Return: "+str(self._portfolio_return(self._inv_distribution_list)))
        print("Portfolio Risk: "+str(self._portfolio_risk(self._inv_distribution_list)))
        print("----------------------------------------------------------------")
        print("Optimization Maximize Portfolio Return")
        print("Method: "+method)
        print("Investment Distribution List: ")
        #print(solution_max_return)
        print(str(solution_max_return.x)+"= "+str(sum(solution_max_return.x)))
        print("Portfolio Return: "+str(self._portfolio_return(solution_max_return.x)))
        print("Portfolio Risk: "+str(self._portfolio_risk(solution_max_return.x)))
        print("----------------------------------------------------------------")
        print("Optimization Minimize Portfolio Risk")
        print("Method: "+method)
        print("Investment Distribution List: ")
        #print(solution_min_risk)
        print(str(solution_min_risk.x)+"= "+str(sum(solution_min_risk.x)))
        print("Portfolio Return: "+str(self._portfolio_return(solution_min_risk.x)))
        print("Portfolio Risk: "+str(self._portfolio_risk(solution_min_risk.x)))
        print("----------------------------------------------------------------")
        print("Optimization Maximize Portfolio Return considering Risk")
        print("Method: "+method)
        print("Investment Distribution List: ")
        #print(solution_max_return_min_risk)
        print(str(solution_max_return_min_risk.x)+"= "+str(sum(solution_max_return_min_risk.x)))
        print("Portfolio Return: "+str(self._portfolio_return(solution_max_return_min_risk.x)))
        print("Portfolio Risk: "+str(self._portfolio_risk(solution_max_return_min_risk.x)))
        plt.hist(self._expected_return_dict["INTC"], color="blue",edgecolor="black",bins=100)
        plt.hist(self._expected_return_dict["CSCO"], color="red",edgecolor="black",bins=100)
        #plt.show()

        print("Genetic Algorithm")
        ga = GeneticAlgorithm(
            minimize_fitness_function= self.objective_maximize_return,
            x0=x0,
            bounds=bounds,
            constraints=constraints,
            population_size=20,
            mutation_rate=0.4,
            max_iterations=10
        )

        SAVE_FILE_NAME = "../tempfiles/MarkowitzPortResults.xlsx"
        with pandas.ExcelWriter(SAVE_FILE_NAME) as writer:
            pandas.DataFrame(stock_price_dict).astype("float64").to_excel(writer, sheet_name="Stock Prices")
            statistics_df.astype("float64").to_excel(writer, sheet_name="Statistics")
            covariance_matrix_df.astype("float64").to_excel(writer, sheet_name="Covariance Matrix")
            correlation_matrix_df.astype("float64").to_excel(writer, sheet_name="Correlation Matrix")


def fitness(x):
    x1 = [x[i]/(i+1) for i in range(len(x))]
    return sum(x1)

def main():
    #mp = MarkowitzPortofolio()
    GeneticAlgorithm.test()




if __name__ == "__main__":
    main()