import re
import sys

# Queues in Python
class Node:
    _value = None
    def __init__(self, value):
        self._value = value
    def getValue(self):
        return self._value
    def setValue(self,value):
        self._value = value
    def __str__(self):
        return str(self._value)

class DoubleLinkedListNode(Node):
    previousNode = None
    nextNode = None
    def __init__(self, value):
        super(DoubleLinkedListNode,self).__init__(value)
    def setPreviousNode(self,previousNode):
        self.previousNode = previousNode
    def setNextNode(self,nextNode):
        self.nextNode = nextNode
    def getPreviousNode(self):
        return self.previousNode
    def getNextNode(self):
        return self.nextNode

class PriorityQueueNode(DoubleLinkedListNode):
    HIGH_PRIORITY = 2
    MEDIUM_PRIORITY = 1
    LOW_PRIORITY = 0
    DEFAULT_TIMEOUT = 30
    priority = 0
    timeout = 0
    ttl = 0

    def __init__(self,value,priority,timeout):
        super(PriorityQueueNode,self).__init__(value)
        self.priority = priority
        self.ttl = timeout
        self.timeout = timeout

    def getPriority(self):
        return self.priority

    def setPriority(self, priority):
        self.priority = priority

    def getTimout(self):
        return self.timeout

    def setTimeout(self, timeout):
        self.timeout = timeout

    def prioritize(self):
        if self.ttl > 0:
            self.ttl -= 1
        else:
            self.ttl = self.timeout
            if self.priority < PriorityQueueNode.HIGH_PRIORITY:
                self.priority += 1
#        print("----------prioritize() "+str(self))

    def getBestPriorityNode(self, priorityQueueNode):
        if self.getPriority() >= priorityQueueNode.getPriority():
            return self
        else:
            return priorityQueueNode

    def __str__(self):
        return "(value:"+str(self._value)+" | priority:"+str(self.priority)+" | ttl:"+str(self.ttl)+")"

class BinaryTreeNode(Node):
    _parentNode = None
    _leftNode = None
    _rightNode = None

    def __init__(self,value):
        super(BinaryTreeNode,self).__init__(value)

    def getParentNode(self):
        return self.parentNode
    def setParentNode(self,binaryTreeNode):
        self._parentNode=binaryTreeNode
    def getLeftNode(self):
        return self._leftNode
    def setLeftNode(self,binaryTreeNode):
        self._leftNode = binaryTreeNode
    def getRightNode(self):
        return self._rightNode
    def setRightNode(self,binaryTreeNode):
        self._rightNode=binaryTreeNode

    def isLeaf(self):
        return self._leftNode == None and self._rightNode == None

    def getSize(self):
        size = 0
        if self._leftNode != None:
            size += self._leftNode.getSize()
        if self._rightNode != None:
            size += self._rightNode.getSize()
        return size + 1

    def getBalance(self):
        balance = 0
        if self._leftNode != None:
            balance = self._leftNode.getBalance() - 1
        if self._rightNode != None:
            balance = self._rightNode.getBalance() + 1
        return balance

    def __str__(self):
        strBuffer = str(self._value)
        if(self._leftNode!=None):
            str += "("+str(self._leftNode)+")"
        if(self._rightNode!=None):
            str += "("+str(self._rightNode)+")"
        return strBuffer

class List:
    firstNode = None
    lastNode = None

    def __init__(self):
        self.flush()

    def flush(self):
        self.firstNode = None
        self.lastNode = None

    def getSize(self):
        if self.isEmpty():
            return 0
        else:
            return len(self.toList())
    def isEmpty(self):
        if self.firstNode == None and self.lastNode == None:
            return True
        return False

    def isSingle(self):
        if self.firstNode.getNextNode() == None and self.lastNode.getPreviousNode() == None:
            return True
        return False

    def toList(self):
        list = []
        if not self.isEmpty():
            node = self.firstNode
            list.append(node)
            while node.getNextNode() != None:
                node = node.getNextNode()
                list.append(node)
        return list

    def toStrList(self):
        list = self.toList()
        strList = []
        for l in list:
            strList.append(str(l))
        return strList

    def __str__(self):
        strBuffer = "< size: "+str(self.getSize())+ " | content: "
        strBuffer += str(self.toStrList())+" >"
        return strBuffer

class DoubleLinkedList(List):
    def __init__(self):
        super(DoubleLinkedList,self).__init__()

    def popFirst(self):
        if self.isEmpty():
            return None
        elif self.isSingle():
            value = self.firstNode.getValue()
            self.flush()
            return value
        else:
            value = self.firstNode.getValue()
            newFirstNode = self.firstNode.getNextNode()
            newFirstNode.setPreviousNode(None)
            self.firstNode = newFirstNode
            return value

    def popLast(self):
        if self.isEmpty():
            return None
        elif self.isSingle():
            value = self.lastNode.getValue()
            self.flush()
            return value
        else:
            value = self.lastNode.getValue()
            newLastNode = self.lastNode.getPreviousNode()
            newLastNode.setNextNode(None)
            self.lastNode = newLastNode
            return value

    def pushFirst(self, value):
        newNode = DoubleLinkedListNode(value)
        if self.isEmpty():
            self.firstNode = newNode
            self.lastNode = newNode
        else:
            self.firstNode.setPreviousNode(newNode)
            newNode.setNextNode(self.firstNode)
            self.firstNode = newNode

    def pushLast(self, value):
        newNode = DoubleLinkedListNode(value)
        if self.isEmpty():
            self.firstNode = newNode
            self.lastNode = newNode
        else:
            self.lastNode.setNextNode(newNode)
            newNode.setPreviousNode(self.lastNode)
            self.lastNode = newNode

    def testPushFirst(self, value):
        self.pushFirst(value)
        print("Pushed first value: " + str(value) + "\tContent: " + str(self))

    def testPushLast(self, value):
        self.pushLast(value)
        print("Pushed last value: " + str(value) + "\tContent: " + str(self))

    def testPopFirst(self):
        print("Popped last value: " + str(self.popFirst()) + "\tContent: " + str(self))

    def testPopLast(self):
        print("Popped last value: " + str(self.popLast()) + "\tContent: " + str(self))

    def testPopLastEverything(self):
        print("Pop Last Everything")
        while (not self.isEmpty()):
            self.testPopLast()

    def testPopFirstEverything(self):
        print("Pop First Everything")
        while (not self.isEmpty()):
            self.testPopFirst()

class Queue(DoubleLinkedList):
    def __init__(self):
        super(Queue,self).__init__()

    def push(self, value):
        self.pushFirst(value)

    def pop(self):
        return self.popLast(self)

    def testPush(self,value):
        self.push(value)
        print("Pushed value: " + str(value) + "\tContent: " + str(self))

    def testPop(self):
        value = self.pop(value)
        print("Popped value: " + str(value) + "\tContent: " + str(self))

    def testPopEverything(self):
        self.testPopLastEverything()

    def test(self):
        print("-------------------Begin Queue Test-----------------")
        print("Initial test size and content---------------------------")
        print("Queue size: " + str(self.getSize()))
        print("Queue content: " + str(self))
        print("Secondary test push and pop values----------------------")
        self.testPush(2)
        self.testPush(8)
        self.testPush(3.14)
        self.testPush("Mama mía")
        self.testPopEverything()
        print("-------------------End Queue Test-----------------")

class Stack(DoubleLinkedList):
    def __init__(self):
        super(Stack,self).__init__()

    def push(self,value):
        self.pushLast(value)

    def pop(self):
        return self.popLast()

    def testPush(self,value):
        self.push(value)
        print("Pushed value: " + str(value) + "\tContent: " + str(self))

    def testPop(self):
        value = self.pop()
        print("Popped value: " + str(value) + "\tContent: " + str(self))

    def testPopEverything(self):
        self.testPopLastEverything()

    def test(self):
        print("-------------------Begin Stack Test--------------------")
        print("Initial test size and content---------------------------")
        print("Stack size: " + str(self.getSize()))
        print("Stack content: " + str(self))
        print("Secondary test push and pop values----------------------")
        self.testPush(2)
        self.testPush(8)
        self.testPush(3.14)
        self.testPush("Mama mía")
        self.testPopEverything()
        print("-------------------End Stack Test-----------------")

#QueuePriorityList pops objects considering the highest priority first, and then the age.
#Its a requisite no packet die for starvation if it has low priority
class PriorityQueue(List):
    def __init__(self):
        super(PriorityQueue,self).__init__()

    def push(self,value,priority):
        node = PriorityQueueNode(value,priority,PriorityQueueNode.DEFAULT_TIMEOUT)
        if self.isEmpty():
            self.firstNode = node
            self.lastNode = node
        else:
            self.prioritizeNodes()
            self.firstNode.setPreviousNode(node)
            node.setNextNode(self.firstNode)
            self.firstNode = node

    def pop(self):
        tmpNode = self.lastNode
        popNode = tmpNode
        if self.isEmpty():
            return None
        elif self.isSingle():
            self.flush()
            return tmpNode
        else:
            while True:
                tmpNode = tmpNode.getPreviousNode()
                if tmpNode != None:
                    popNode = popNode.getBestPriorityNode(tmpNode)
                else:
                    break
            self.removeNode(popNode)
            return popNode

    def removeNode(self, priorityQueueNode):
        previousNode = priorityQueueNode.getPreviousNode()
        nextNode = priorityQueueNode.getNextNode()

        if self.isEmpty():
            return
        elif self.isSingle():
            self.flush()
        elif previousNode != None and nextNode != None:
            previousNode.setNextNode(nextNode)
            nextNode.setPreviousNode(previousNode)
        elif previousNode != None and nextNode == None:
            previousNode.setNextNode(None)
            self.lastNode = previousNode
        elif previousNode == None and nextNode != None:
            nextNode.setPreviousNode(None)
            self.firstNode = nextNode

    def prioritizeNodes(self):
        if not self.isEmpty() or self.isSingle():
            tmpNode = self.lastNode
            while True:
                tmpNode.prioritize()
                tmpNode = tmpNode.getPreviousNode()
                if tmpNode == None:
                    break

    def testPush(self, value, priority):
        self.push(value,priority)
        print("Pushed value:" + str(value) + "\tPriority:"+str(priority)+"\tQueue Content:" + str(self))

    def testPushMultiple(self,value,priority,number):
        i=0
        while i<number:
            self.testPush(str(value)+str(i),priority)
            i+=1

    def testPop(self):
        tmpNode = self.pop()
        print("Popped value:"+str(tmpNode)+"\tQueue Content:" + str(self))

    def testPopEverything(self):
        print("Pop Everything")
        while not self.isEmpty():
            self.testPop()

    def test(self):
        print("-------------------Begin Priority Queue Test--------------------")
        print("Initial test size and content---------------------------")
        print("Priority Queue size: " + str(self.getSize()))
        print("Priority Queue content: " + str(self))
        print("Secondary test push and pop values----------------------")
        self.testPushMultiple("LOW",PriorityQueueNode.LOW_PRIORITY,10)
        self.testPushMultiple("MEDIUM",PriorityQueueNode.MEDIUM_PRIORITY,10)
        self.testPushMultiple("HIGH",PriorityQueueNode.HIGH_PRIORITY,20)
        self.testPopEverything()
        print("-------------------End Priority Queue Test-----------------")

class BinaryTree:
    _rootNode = None
    _digit_symbol = r"01234567890"
    _negative_symbol = r"-"
    _point_symbol = r"."
    _openparentesis_symbol = r"("
    _closeparentesis_symbol = r")"
    _dictionary = r""+_digit_symbol+_negative_symbol+_point_symbol+_openparentesis_symbol+_closeparentesis_symbol+""

    def __init__(self):
        return

    def isEmpty(self):
        return self._rootNode == None

    def getSize(self):
        return self._rootNode.getSize()

    def getBalance(self):
        return self._rootNode.getBalance()

    def _isInDictionary(self,dictionary,string):
        regexp = r"["+self._dictionary+r"]"
        return re.search(regexp,string) != None

    def _isNumber(self, string):
        #_digit_symbol  11   (^\d+$)
        #_point_symbol + _digit_symbol  .11 (^\.\d+$)
        #_digit_symbol + _point_symbol  11. (^\d+\.$)
        #_digit_symbol + _point_symbol + digit_symbol   11.11   (^\d+\.\d+$)
        #_negative_symbol + _digit_symbol   -11 (^\-\d+$)
        #_negative_symbol + _point_symbol + _digit_symbol  -.11 (^\-\.\d+$)
        #_negative_symbol + _digit_symbol + _point_symbol  -11. (^\-\d+\.$)
        #_negative_symbol + _digit_symbol + _point_symbol + digit_symbol   -11.11   (^\-?\d+\.\d+$)
        # (^\-?\d+$)|(^\-?\.\d+$)|(^\-?\d+\.$)|(^\-?\d+\.\d+$)
        regexp = r"(^\-?\d+$)|(^\-?\.\d+$)|(^\-?\d+\.$)|(^\-?\d+\.\d+$)"
        return re.search(regexp,string) != None

    def _toTokenedList(self, stringedTree):
        tokenList = []

        #Verify is not None
        if stringedTree == None:
            return None

        #Verify the variable is a string.
        if type(stringedTree) != str:
            return None

        #Verify every character in string exists in the dictionary.
        if not self._isInDictionary(self._dictionary,stringedTree):
            return None

        #Verify there is a correct number of parentesis.
        if stringedTree.count(self._openparentesis_symbol) != stringedTree.count(self._closeparentesis_symbol):
            return None

        #Verify the stringedTree begins with the correct character.
        if stringedTree[0] == self._openparentesis_symbol or stringedTree[0] == self._closeparentesis_symbol:
            return None

        strValue = ""
        for c in stringedTree:
            if c == self._openparentesis_symbol:
                if(len(strValue)>0):
                    tokenList.append(strValue)
                strValue = ""
                tokenList.append(c)
            elif c == self._closeparentesis_symbol:
                if(len(strValue)>0):
                    tokenList.append(strValue)
                strValue = ""
                tokenList.append(c)
            else:
                strValue += c
        if (len(strValue)>0):
            tokenList.append(strValue)
        return tokenList

    def _toTreeList(self, tokenedList):
        treeList = []
        if tokenedList == None:
            return None
        if type(tokenedList) != list:
            return None

        token = tokenedList.pop(0)
        subTokenedList = []
        if token == self._openparentesis_symbol:
            count = 1
            for token2 in tokenedList:
                if token2 == self._openparentesis_symbol:
                    count+=1
                elif token2 == self._closeparentesis_symbol:
                    count-=1
                if count == 0:
                    subTreeList = self._toTreeList(subTokenedList)
                    if subTreeList == None:
                        return None
                    else:
                        treeList.append(subTreeList)
                    subTokenedList = []
        elif token == self._closeparentesis_symbol:
            return None
        else:
            treeList.append(token)
        if len(tokenedList) == 0:
            return treeList





    def parseTree(self, stringedTree):
        tokenedList = self._toTokenedList(stringedTree)
        return self._toTreeList(tokenedList)

    def getStrProperties(self):
        strBuffer = "Binary Tree properties---------------------------"
        strBuffer += "\n"+self.__str__()
        strBuffer +="\nSize: " + str(self.getSize())
        strBuffer +="\nBalance " + str(self.getBalance())
        return strBuffer

    def __str__(self):
        strBuffer = self._rootNode.__str__()
        return strBuffer

    def _testIsNumber(self):
        n1 = "111"
        n2 = ".111"
        n3 = "111."
        n4 = "111.111"
        n5 = "-111"
        n6 = "-.111"
        n7 = "-111."
        n8 = "-111.111"
        n9 = "--1."
        n10 = "1..1"
        n11 = "1-1"
        print("testIsNumber--------------------------------")
        print("n1: "+n1+" isNumber:"+str(self._isNumber(n1)))
        print("n2: "+n2+" isNumber:"+str(self._isNumber(n2)))
        print("n3: "+n3+" isNumber:"+str(self._isNumber(n3)))
        print("n4: "+n4+" isNumber:"+str(self._isNumber(n4)))
        print("n5: "+n5+" isNumber:"+str(self._isNumber(n5)))
        print("n6: "+n6+" isNumber:"+str(self._isNumber(n6)))
        print("n7: "+n7+" isNumber:"+str(self._isNumber(n7)))
        print("n8: "+n8+" isNumber:"+str(self._isNumber(n8)))
        print("n9: "+n9+" isNumber:"+str(self._isNumber(n9)))
        print("n10: "+n10+" isNumber:"+str(self._isNumber(n10)))
        print("n11: "+n11+" isNumber:"+str(self._isNumber(n11)))

    def _testToTokenedList(self):
        stringedList1 = "a(b)(c)"
        stringedList2 = "aa(bb(dd)(ee))(cc(ff)(gg))"
        stringedList3 = "a(b)()"
        stringedList4 = "a()(c)"
        stringedList5 = "a(b)"
        stringedList6 = "a(b)(()"
        print("stringedList1: "+stringedList1+"\t"+str(self._toTokenedList(stringedList1)))
        print("stringedList2: "+stringedList2+"\t" + str(self._toTokenedList(stringedList2)))
        print("stringedList3: "+stringedList3+"\t" + str(self._toTokenedList(stringedList3)))
        print("stringedList4: "+stringedList4+"\t" + str(self._toTokenedList(stringedList4)))
        print("stringedList5: "+stringedList5+"\t" + str(self._toTokenedList(stringedList5)))
        print("stringedList6: "+stringedList6+"\t" + str(self._toTokenedList(stringedList6)))

    def test(self):
        print("-------------------Begin BinaryTree Test--------------------")
        self._testIsNumber()
        self._testToTokenedList()
        print("Secondary test push and pop values----------------------")

        strtree1 = "50(25)(75)"
        bt1 = BinaryTree()
        #bt1 = bt1.parseTree(strtree1)
        #print(bt1.getStrProperties())

        strtree2 = "50.2(25(20)(55))(75(70)(80.20))"
        bt2 = BinaryTree()
        #bt2 = bt2.parseTree(strtree2)
        #print(bt2.getStrProperties())

        strtree3 = "50.2(25(20)(55))/(75(70)(80.20))"
        bt3 = BinaryTree()
        #bt3 = bt3.parseTree(strtree3)
        #print(bt3.getStrProperties())

        print("-------------------End BinaryTree Test-----------------")


def main():
    print("---------------Data Structures--------------")
    queue = Queue()
    queue.test()

    stack = Stack()
    stack.test()

    pqueue = PriorityQueue()
    pqueue.test()

    #bTree = BinaryTree() < --- Wasnt able to finish btree need more regular expression knowledge.
    #bTree.test()
