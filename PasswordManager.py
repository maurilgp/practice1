import sys,argparse,pyperclip
class PasswordManager:
    _PASSWORD_DATABASE = {"vpn" : "vpnpassowrd20394808",
                          "email" : "emailpassword234u0942384098",
                          "blog" : "blogpassword87643289",
                          "remotepc" : "remotepcpassword9237892834"
                          }

    def __init__(self):
        parser = argparse.ArgumentParser(prog="PasswordManager", description="Copies specific saved passwords to the clipboard.")
        parser.add_argument("passwordtype",help="Copies specified password to clipboard: vpn, email, blog, remotepc")
        args = parser.parse_args()
        print("args: "+str(args))
        print("args.passwordtype: "+str(args.passwordtype))
        passwordvalue = self._PASSWORD_DATABASE.get(args.passwordtype)

        if passwordvalue != None:
            print("passwordvalue: " + passwordvalue)
            pyperclip.copy(passwordvalue)
            print(args.passwordtype+" password copied to clipboard, you can paste it in the required field")
        else:
            print(args.passwordtype+" type doesn't exists, please specify a valid type password.")
