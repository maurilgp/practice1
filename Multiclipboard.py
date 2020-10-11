#This program copies text to a clipboard and store it to a file for later usage
#usage:
# py main.py save id  saves what is in the clipboard with a specified id
# py main.py read id  copies to the clipboard what is queried by the id

import pyperclip, argparse, sys, shelve, re

class Multiclipboard:
    FILENAME = ".\\tempfiles\\multiclipboard"
    DICTIONARY = "clipboard_dict"
    LOAD = "load"
    REMOVE = "remove"
    SAVE = "save"
    PRINT = "print"

    def __init__(self):
        self.initialize()
        parser = argparse.ArgumentParser(description="Application to save clipboard data.")
        parser.add_argument("action", help="Action to perform with the clipboard: load / save ")
        parser.add_argument("--key", help="Name of the variable to store o retrieve the value.")
        args = parser.parse_args()
        action = args.action
        key = args.key

        if args.action == self.LOAD:
            if self.isvalidkey(args.key):
                self.load(args.key)
            else:
                print("Key name is invalid, please use alphanumerical characters.")
        elif args.action == self.SAVE:
            if self.isvalidkey(args.key):
                self.save(args.key)
            else:
                print("Key name is invalid, please use alphanumerical characters.")
        elif args.action == self.REMOVE:
            if self.isvalidkey(args.key):
                self.remove(args.key)
            else:
                print("Key name is invalid, please use alphanumerical characters.")
        elif args.action == self.PRINT:
            self.display()
        else:
            print("No valid action was typed, use \"load\", \"save\", \"remove\" or \"print\".")
            return

    def initialize(self):
        with shelve.open(self.FILENAME) as sf:
            #File must exists and at least contain a variable.
            sf["a"]=0
            #Generate the dictionary if does't exist.
            if not self.DICTIONARY in sf:
                sf[self.DICTIONARY] = {}

    def isvalidkey(self, key):
        pattern = "^[\w\d]+$"
        search = re.search(pattern,key)
        if search != None:
            return True
        else:
            return False

    def load(self, key):
        with shelve.open(self.FILENAME) as sf:
            if sf != None:
                clipboard_dict = sf[self.DICTIONARY]
                value = clipboard_dict.get(key)
                if value != None:
                    pyperclip.copy(value)
                    print("Value from key \""+key+"\" copied to clipboard.")
                else:
                    print("Key \""+str(key)+"\" doesn't exist, use print to display stored values.")

    def save(self, key):
        value = pyperclip.paste()
        if(value != None):
            with shelve.open(self.FILENAME) as sf:
                if sf != None:
                    clipboard_dict = sf[self.DICTIONARY]
                    clipboard_dict[key] = value
                    sf[self.DICTIONARY] = clipboard_dict
                    print("Value stored on key \"" + str(key) + "\"")
        else:
            print("No value on the clipboard to copy.")

    def remove(self, key):
        with shelve.open(self.FILENAME) as sf:
            if sf != None:
                clipboard_dict = sf[self.DICTIONARY]
                if key in clipboard_dict:
                    del clipboard_dict[key]
                    sf[self.DICTIONARY] = clipboard_dict
                    print("Value from key \""+str(key)+"\" deleted.")
                else:
                    print("Key \""+str(key)+"\" not found.")


    def display(self):
        with shelve.open(self.FILENAME) as sf:
            if sf != None:
                clipboard_dict = sf[self.DICTIONARY]
                if clipboard_dict != None:
                    keys = list(clipboard_dict.keys())
                    print("---------------Clipboard content------------")
                    for k in keys:
                        print(str(k)+": "+clipboard_dict.get(k))
                    print("--------------------------------------------")