import os, re, shelve, pprint
import numpy as np
import matplotlib.pyplot as plt

class FileExercises:
    def __init__(self):
        #self.fileExcersize1()

        #dirammount = self.explorerdisk("C:\\")
        #print("Directories found: "+str(dirammount))

        #numfiles = self.searchFile("C:\\", r"\.txt$")
        #print("Files found: "+str(numfiles))

        #self.paths()

        self.loadsettings()

    def fileExcersize1(self):
        print("os.path: "+str(os.path))
        print("Current directory os.cwd(): "+str(os.getcwd()))
        dircontent = os.listdir()
        print("List content of the current directory listdir(): "+str(dircontent))
        for d in dircontent:
            regex_pattern = r"[\w\W]+\.py$"
            s = re.search(regex_pattern, d)
            if s != None:
                print(s.group())

        os.chdir("C:\\")
        print(os.getcwd())

    def explorerdisk(self,initialpath):
        dirammount = 0
        os.chdir(initialpath)
        print("Current directory: "+os.getcwd())
        filesindir = os.listdir()
        #print("Files in directory: "+str(filesindir))
        directories = []
        for f in filesindir:
            if os.path.isdir(f):
                directories.append(f)
                dirammount += 1
        #print("Directories in directory: "+str(directories))

        for d in directories:
            nextpath = initialpath+d+"\\"
            try:
                dirammount += self.explorerdisk(nextpath)
            except Exception:
                print("Error by attempting to enter:"+nextpath)

        return dirammount

    def searchFile(self,path , filename):
        #print("Searching for: "+filename)
        numfiles = 0
        os.chdir(path)
        currentdirectory = os.getcwd()
        #print("Current directory: "+str(currentdirectory))
        files = os.listdir()
        #Find files in current directory
        compile = re.compile(filename)
        directories = []
        for f in files:
            search = compile.search(f)
            if(search != None):
                print("File found : "+currentdirectory+"\\"+f)
                numfiles += 1
            if os.path.isdir(f):
                directories.append(f)

        #Navigate to other directories.
        for d in directories:
            newpath = currentdirectory+"\\"+d
            try:
                 numfiles += self.searchFile(newpath,filename)
            except Exception:
                print("Error entering directory: "+newpath)
        return numfiles

    def paths(self):
        path = r"."
        print("os.path.abspath(path): "+str(os.path.abspath(path)))
        path = r".\tempfiles"
        print("os.path.abspath(path): "+str(os.path.abspath(path)))
        path = r".\tempfiles"
        print("os.path.isabs(path): "+str(os.path.isabs(path)))
        print("os.path.isabs(\"C:\\Users\\amigo\\PycharmProjects\\practice1\\tempfiles\"): "+str(os.path.isabs("C:\\Users\\amigo\\PycharmProjects\\practice1\\tempfiles")))
        path = r"C:\Users\amigo\PycharmProjects\practice1\main.py"
        print("os.path.basename(path): "+str(os.path.basename(path)))
        print("os.path.dirname(path): "+str(os.path.dirname(path)))

        path = r"C:\Windows\System32"
        listdir = os.listdir(path)
        print(path + " " + str(listdir))
        path = r"C:\Windows\System32\cmd.exe"
        print("os.path.getsize("+path+"): "+str(os.path.getsize(path)))
        print("os.path.exists("+path+"): "+str(os.path.exists(path)))
        path = r"D:"
        print("os.path.exists("+path+"): "+str(os.path.exists(path)))

    def loadsettings(self):
        sfile = r".\tempfiles\settings"

        with shelve.open(sfile) as sf:
            pepe="pecas"
            sf["pepe"]=pepe
            sf.close()

        with shelve.open(sfile) as sf:
            print(sf["pepe"])
            print(sf)
            sf.close()

        filename = "FileManager.py"
        with open(filename,"r") as f:
            content = f.read()
            with shelve.open("settings") as sf:
                sf[filename] = content

        csvfile = r".\tempfiles\SPY2.csv"
        shelvefile = r".\tempfiles\SPY"
        with open(csvfile, "r") as f:
            SPY = f.readlines()
            if SPY != None:
                if len(SPY) > 0:
                    table = []
                    fields = None
                    for i in range(len(SPY)):
                        columns = SPY[i].split(",")
                        if(i == 0):
                            fields = columns
                        else:
                            row = {}
                            for j in range(len(columns)):
                                row[fields[j]] = columns[j]
                            table.append(row)
                    with shelve.open(shelvefile) as sf:
                        sf["table"] = table
                    with shelve.open(shelvefile) as sf:
                        table = sf["table"]
                        print(table)
                        x = []
                        y = []
                        for t in table:
                            x.append(t["Date"])
                            y.append(float(t["Open"]))
                        pprint.pprint(x)
                        pprint.pprint(y)
                        fig, ax = plt.subplots()
                        #ax.plot([1,2,3,4,5],[1,4,2,3,7])
                        ax.plot(x,y)
                        plt.show()









class FileReader:
    def __init__(self):
        filepath = r"C:\Users\amigo\PycharmProjects\practice1\SPY.csv"
        mode = "r"
        self.readTextFile(filepath,mode)

    def readTextFile(self,filepath,mode):
        print("filepath: "+filepath)
        print("mode: "+mode)
        with open(filepath,mode) as file:#file = open(filepath,mode)
            print(str(file))
            content = file.read()
            print("----------Filecontent:-----------")
            print(content)
            print("-------------EOF-----------------")
            file.close()

