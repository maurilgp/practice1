import numpy

def main():

    array = []
    for i in range(10):
        if i == 0:
            array.append(numpy.array([1,2,3]))
        else:
            array.append(numpy.array([array[i-1],array[i-1],array[i-1]]))
        print("############################")
        print(array[i])
        print("Dimensions: "+str(array[i].ndim))
        print("Shape: "+str(array[i].shape))
        print("Size: "+str(array[i].size))
