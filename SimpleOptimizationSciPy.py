# Maximize f(x) = x
# s.t. 0<=x<=8
# x0 = 0
#SciPy does not support maximization inverse minimization can override the problem.
# Minimize f(x) = -x

import numpy, scipy.optimize, math


def print_variables(x):
    string = ""
    for i in range(len(x)):
        string += "x"+str(i+1)+"="+str(x[i])
        if i < len(x) -1:
            string += ", "
    print(string)


def print_var_info(name, value):
    print(name+"= "+str(value)+" "+str(type(value)))


def objective(x):
    # Minimize f(x) = -x
    return -x[0]

def constraint1(x):
    return 0


def main():
    x0 = list([0.0])
    b = (0.0, 8.0)
    bounds = [b]
    con1 = {"type": "eq", "fun": constraint1}
    constraints = [con1]

    #print_var_info("x0", x0)
    #print_var_info("b", b)
    #print_var_info("bounds", bounds)
    #print_var_info("con1", con1)
    #print_var_info("constraints", constraints)
    method = "Powell"
    solution = scipy.optimize.minimize(objective, x0, method=method, bounds=bounds)
    print("----------------------------------------------------------------")
    print("Optimization Exercise")
    print("Maximize f(x) = x")
    print("s.t. 0<=x<=8")
    print("x0 = 0")
    print("----------------------------------------------------------------")
    print("Suboptimal Solution")
    print("Variables: ")
    print_variables(x0)
    print("Value: "+str(objective(x0)))
    print("----------------------------------------------------------------")
    print("Method: "+method)
    print(solution)
    print("----------------------------------------------------------------")
    print("Optimal Solution")
    print("Variables: ")
    print_variables(solution.x)
    print("Value: "+str(objective(solution.x)))

if __name__ == "__main__":
    main()