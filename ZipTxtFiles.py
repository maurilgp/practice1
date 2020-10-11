# The purpose of this class is to find txt files in the disk and copy them in to zip files.
# Black list of directories to exclude should exist.
#
import os, zipfile, re, sys, datetime
class ZipTxtFiles:
    FILEPATH = os.path.abspath(".\\tempfiles")
    now = datetime.datetime.now()
    LOGFILE = "ZIPTXTFILES-" + str(now.year) + "-" + str(now.month) + "-" + str(now.day) + ".LOG"

    def __init__(self):
        self.proceeslogfile("-----------------BEGIN PROGRAM EXECUTION---------------")
        ZIPFILENAME = "zipfile.zip"
        PASSWORD = "lalaland"
        pattern = r"\.txt$"
        txtfiles = self.searchfiles("C:\\", pattern)
        self.proceeslogfile(str(len(txtfiles))+" textfiles found")
        self.createzipfile(self.FILEPATH, ZIPFILENAME, txtfiles, PASSWORD)
        self.readzipfile(self.FILEPATH, ZIPFILENAME, PASSWORD)
        self.proceeslogfile("-----------------END OF PROGRAM EXECUTION---------------")

    def getdir(self, path):
        #print("extractdir("+path+")")
        directories = []
        try:
            os.chdir(path)
            files = os.listdir()
            for f in files:
                if os.path.isdir(f):
                    #print("Directory found: "+str(os.path.abspath(f)))
                    directories.append(os.path.abspath(f))
        except Exception:
            LOGSTR = "getdir(" + path + ")\n"
            LOGSTR += "Error getting dir path:" + path + ")\n"
            LOGSTR += str(sys.exc_info()[0]) + "\n"
            self.proceeslogfile(LOGSTR)
        return directories

    def getfiles(self, path, filename):
        extractedfiles = []
        try:
            os.chdir(path)
            files = os.listdir()
            comp = re.compile(filename)
            #print("Directory size: "+str(len(files)))
            for f in files:
                search = comp.search(f)
                if search != None:
                    self.proceeslogfile("File found: "+str(os.path.abspath(f)))
                    extractedfiles.append(os.path.abspath(f))
        except Exception:
            LOGSTR = "getfiles("+path+","+filename+")\n"
            LOGSTR += "Error getting file path:"+path+" filename:"+filename + "\n"
            LOGSTR += str(sys.exc_info()[0]) + "\n"
            self.proceeslogfile(LOGSTR)
        return extractedfiles

    def searchfiles(self, path, filename):
        files = self.getfiles(path, filename)
        directories = self.getdir(path)
        for d in directories:
            files += self.searchfiles(d, filename)
        return files

    def createzipfile(self, path, filename, files, password):
        bytepassword = bytes(password, "utf-8")
        try:
            os.chdir(path)
            with zipfile.ZipFile(filename, "w") as zf:
                zf.setpassword(bytepassword)
                for f in files:
                    try:
                        LOGSTR = "Compressing: " + f + "\n"
                        self.proceeslogfile(LOGSTR)
                        zf.write(f, compress_type=zipfile.ZIP_DEFLATED)
                    except Exception:
                        LOGSTR = "createzipfile(\n"
                        LOGSTR += "Error compressing file: " + f + "\n"
                        LOGSTR += str(sys.exc_info()[0]) + "\n"
                        self.proceeslogfile(LOGSTR)
            LOGSTR = "Zipfile creation finished: " + filename
            self.proceeslogfile(LOGSTR)
        except Exception:
            LOGSTR = "createzipfile(\n" + str(path) + "," + str(filename) + "," + str(files) + "," + str(password) + ")\n"
            LOGSTR += "Error creating zip file.\n"
            LOGSTR += str(sys.exc_info()[0]) + "\n"
            self.proceeslogfile(LOGSTR)

    def readzipfile(self, path, filename, password):
        bytepassword = bytes(password, "utf-8")
        try:
            os.chdir(path)
            with zipfile.ZipFile(filename,"r") as zf:
                files = zf.namelist()
                for f in files:
                    try:
                        print(f)
                        info = zf.getinfo(f)
                        percent = round(float(info.compress_size) / float(info.file_size) * 100.0, 2)
                        self.proceeslogfile("Extracting: "+filename+str(info.file_size)+"\t"+str(info.compress_size)+"\t"+str(percent)+"%\t"+str(info.compress_type)+"\t"+str(info.comment)+"\t"+str(info.file_size)+str(info.date_time)+"\n")
                        zf.extract(f, path, bytepassword)
                    except Exception:
                        LOGSTR = "readzipfile(" + path + "," + filename + ", " + password + ")\n"                       ")\n"
                        LOGSTR += str(sys.exc_info()[0]) + "\n"
                        self.proceeslogfile(LOGSTR)
        except Exception:
            LOGSTR = "readzipfile(" + path + "," + filename + ", " + password + ")\n"
            LOGSTR += "Error reading zipfile: "+path+")\n"
            LOGSTR += str(sys.exc_info()[0]) + "\n"
            self.proceeslogfile(LOGSTR)

    def proceeslogfile(self, log):
        loglines = log.split("\n")
        LOGSTR = ""
        now = datetime.datetime.now()
        for l in loglines:
            LOGSTR += now.strftime("%Y-%m-%d %H:%M:%S") + " " + l + "\n"
        print(LOGSTR)
        logfile = self.FILEPATH+"\\"+self.LOGFILE
        print(logfile)
        with open(logfile,"a") as f:
            f.write(LOGSTR)
