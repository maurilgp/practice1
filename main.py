#This is the main file, this project itself doesn't has the purpose of doing small python excercises during the learning proceess.
#Every file represents a different exercises and a class with the same name will contain the exercise code to execute.
import DataStructures
import StringManipulationExercise
import FileManager
from RegularExpressions import RegularExpressions
from PasswordManager import PasswordManager
import MathLibrary
import MatPlotExercises
import RandomQuiz
import Multiclipboard
import ZipTxtFiles
import LoggingExample
import WebDownloader
import ShoppingCart
import ProductFinder
import Afluenta
import SimFinDatabase
import PythonForDataAnalysis_ch02
import Pokemon
import NumPyExcercises
import ANOVA
import OutstandingBalance
import MarkowitzPortfolio
import IntrinsicValue
import FinancialModelingGrepExcercises
import JSONExercises

import sys, pyperclip, logging, unittest


def initialize_logging():
    # set up logging to file
    fn = "temp"
    fm = "a"
    lvl = logging.DEBUG
    fmt = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename=fn, filemode=fm, level=lvl, format=fmt)
    # set up logging to console
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(logging.Formatter(fmt))
    # add the handler to the root logger
    logging.getLogger('').addHandler(sh)
    logger = logging.getLogger(__name__)
    logger.debug("Logging engine initialized, using file: " + fn)



sys.setrecursionlimit(10000)
#initialize_logging()
#logging.getLogger().disabled = True


# DataStructures.main()

# StringManipulationExercise.main()

# Reading files Exercise.
# print("Reading files Exercise.")
# fr = FileManager.FileReader()

# Password Manager Excersize.
# Must be run under terminal "py main.py"
# pm = PasswordManager()

# Regular Expression Excersize.
# print("Regular Expression Excersize.")
# re = RegularExpressions()

# fe = FileExercises()


#fe = FileManager.FileExercises()

#mp = MatPlotExercises.MatplotlibExercises()

#rq = RandomQuiz.RandomQuiz()

#mcb = Multiclipboard.Multiclipboard()

# ztf = ZipTxtFiles.ZipTxtFiles()

# le = LoggingExample.LoggingExample()

# wd = WebDownloader.WebDownloaer()



#c = ShoppingCart.Currency()
#c.test()

#p = ShoppingCart.Product(code="5410063031272",description="Cereal Pralinerepen Glutenvrij",price=4.5)
#print("Product: "+str(p))


#sp = ShoppingCart.ShoppingCart()
#sp.test()

#pf = ProductFinder.ProductFinder()

#sd = SimFinDatabase.SimFinDatabase()

#Afluenta.LoanDatabase()


#PythonForDataAnalysis_ch02.PhytonForDataAnalysis_ch02()

#Pokemon.Pokemon()

#ANOVA.Anova()

#OutstandingBalance.OutstandingBalance()

#MarkowitzPortfolio.MarkowitzPortofolio()

:IntrinsicValue.main()

#NumPyExcercises.main()

#FinancialModelingGrepExcercises.main()

#JSONExercises.main()

