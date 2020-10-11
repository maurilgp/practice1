#This is the main file, this project itself doesn't has the purpose of doing small python excercises during the learning proceess.

import DataStructures
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
import ANOVA

import sys, pyperclip, logging


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
initialize_logging()
#logging.getLogger().disabled = True

# print("---------------Data Structures--------------")
# queue = DataStructures.Queue()
# queue.test()
# stack = DataStructures.Stack()
# stack.test()
# pqueue = DataStructures.PriorityQueue()
# pqueue.test()
# bTree = DataStructures.BinaryTree()
# bTree.test()

# text = "abcdefg"
# print("text[0]\t" + text[0])
# print("text[0:3]\t" + text[0:3])
# print("type([]): " + str(type([])))
# print("str(type([1,2,3])==type([])): " + str(type([1, 2, 3]) == type([])))
# print("list==type([])): " + str(list == type([])))
#
# r = range(10)
# print("r\t" + str(r))
# print("type(r)\t" + str(type(r)))
# for i in r:
#     print(str(i))
#



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

# def funct1(argument1="Hola",argument2="mundo"):
#     print(argument1+" "+argument2)
#
#
# funct1()
# funct1("lalaland","is cool")
# funct1(argument2="is a great game", argument1="vvvvvv")
#
# a=funct1
# a()
# a("111","222")
# a(argument1="123",argument2="456")
#
# def funct2(fasargument):
#     print("--------------")
#     fasargument()
#     print("--------------")
#
#
# funct2(funct1)


# class sum:
#     _sum = 0
#
#     def __init__(self, num1, num2):
#         self._sum = num1 + num2
#
#     def __enter__(self):
#         return self
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         print("done")
#
#
#     def getSum(self):
#         return self._sum
#
#
# with sum(1, 2) as s:
#     print(str(s.getSum()))
#
#
# a = [x for x in range(10)]
# print(str(a))
#
# a = [x for x in range(2,20)]
# print(str(a))
#
# print(str(dir(MathLibrary)))
# print(str(dir(MathLibrary.GeometricShapeAreas)))
# print(str(MathLibrary.sum(1.0,2.0)))
# a = MathLibrary.GeometricShapeAreas()
# print(str(a.square(2.0)))


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

ANOVA.Anova()