def main():
 text = "abcdefg"
 print("text[0]\t" + text[0])
 print("text[0:3]\t" + text[0:3])
 print("type([]): " + str(type([])))
 print("str(type([1,2,3])==type([])): " + str(type([1, 2, 3]) == type([])))
 print("list==type([])): " + str(list == type([])))

 r = range(10)
 print("r\t" + str(r))
 print("type(r)\t" + str(type(r)))
 for i in r:
  print(str(i))
