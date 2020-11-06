import matplotlib.pyplot as plt, numpy, scipy.interpolate as inter
from random import random

def main():
    print("Regression Example")
    x = numpy.array([random() for i in range(1000)])
    y = numpy.array([random() for i in range(1000)])
    y = numpy.array([random()*x[i]**2 for i in range(1000)])
    correlation = numpy.corrcoef(x,y)
    p1 = numpy.polyfit(x,y,1)
    p2 = numpy.polyfit(x,y,2)
    p3 = numpy.polyfit(x,y,3)
    print(x)
    print(y)
    print(p1)
    print(p2)
    print(p3)
    print("Correlation: ")
    print(correlation)
    #plt.legend = "Correlation: " + str(correlation)
    plt.xlabel = "X Axis"
    plt.ylabel = "Y Axis"
    plt.plot(x, y, "yo")
    plt.plot(x, numpy.polyval(p1, x), "r-")
    #plt.plot(x, numpy.polyval(p2, x), "b-")
    #plt.plot(x, numpy.polyval(p3, x), "g-")
    plt.show()


if __name__ == "__main__":
    main()