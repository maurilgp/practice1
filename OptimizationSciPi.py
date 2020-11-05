# Example of Mathematical optimization with python.
# Exercise was done using the following source
# https://apmonitor.com/che263/index.php/Main/PythonOptimization
# min x1*x4*(x1+x2+x3)+x3
# s.t. x1*x2*x3*x4 >= 25
# x1^2+x2^2+x3^2+x4^2 = 40
# 1<= x1,x2,x3,x3,x4 <= 5
# x0 = (1,5,5,1)

import numpy
import scipy.optimize

def print_variables(x):
    string = ""
    for i in range(len(x)):
        string += "x"+str(i+1)+"="+str(x[i])
        if i < len(x) -1:
            string += ", "
    print(string)


def objective(x):
    # min x1*x4*(x1+x2+x3)+x3
    x1, x2, x3, x4 = x[0], x[1], x[2], x[3]
    return x1*x4*(x1+x2+x3)+x3

def constraint1(x):
    #x1*x2*x3*x4 >= 25
    x1, x2, x3, x4 = x[0], x[1], x[2], x[3]
    return x1*x2*x3*x4-25

def constraint2(x):
    #x1^2+x2^2+x3^2+x4^2=40
    x1, x2, x3, x4 = x[0], x[1], x[2], x[3]
    return x1**2+x2**2+x3**2+x4**2-40

def main():
    b = (1.0, 5.0)
    bounds = (b,b,b,b)
    con1 = {"type": "ineq", "fun": constraint1}
    con2 = {"type": "eq", "fun": constraint2}
    constraints = [con1, con2]
    x0 = [1, 5, 5, 1]
    solution = scipy.optimize.minimize(objective, x0, method="SLSQP", bounds=bounds, constraints=constraints)

    print("----------------------------------------------------------------")
    print("Optimization Excersice")
    print("min x1*x4*(x1+x2+x3)+x3")
    print("s.t. x1*x2*x3*x4 >= 25")
    print("     x1^2+x2^2+x3^2+x4^2 = 40")
    print("     1<= x1,x2,x3,x3,x4 <= 5")
    print("x0 = (1,5,5,1)")
    print("----------------------------------------------------------------")
    print_variables(x0)
    print("Suboptimal solution: "+str(objective(x0)))

    print("----------------------------------------------------------------")
    print(solution)
    print("----------------------------------------------------------------")
    print_variables(solution.x)
    print("Optimal solution: "+str(objective(solution.x)))

if __name__ == "__main__":
    main()