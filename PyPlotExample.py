import os, matplotlib.pyplot, numpy



def main():
    filename = os.path.abspath("tempfiles\\data_with_headers.txt")
    data_file = numpy.loadtxt(filename, delimiter=",")
    time = data_file[:,0]


    print("Pyplot Example")
    print("File: "+filename)
    print("Data File")
    print(data_file)


if __name__ == "__main__":
    main()