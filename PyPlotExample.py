import os, matplotlib.pyplot as plt, numpy

def print_array_properties(array):
    print("Dimensions: "+str(array.ndim))
    print("Size: "+str(array.size))
    print("Shape: "+str(array.shape))

def main():
    filename = os.path.abspath("tempfiles\\data_with_headers.txt")
    data_file = numpy.loadtxt(filename, delimiter=",")
    time_column = data_file[:, 0]
    time_column = time_column - time_column[0]
    sensors_array = data_file[:, 1:5]
    average_column = numpy.mean(sensors_array,axis=1)
    my_data = numpy.vstack((time_column, sensors_array.T, average_column))

    print("Pyplot Example")
    print("File: "+filename)
    print("\nData File")
    print(data_file)
    print_array_properties(data_file)
    print("\nTime Column")
    print(time_column)
    print_array_properties(time_column)
    print("\nSensors Array")
    print(sensors_array)
    print_array_properties(sensors_array)
    print("\nAverage")
    print(average_column)
    print_array_properties(average_column)
    print("\nData")
    print(my_data)
    print_array_properties(my_data)

    plt.plot(time_column/60, sensors_array[:, 0], "ro")
    plt.plot(time_column/60, average_column,"bo")
    plt.legend("Sensor 1 Average")
    plt.xlabel("Time (min)")
    plt.ylabel("Values")
    plt.show()


if __name__ == "__main__":
    main()