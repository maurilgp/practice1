import re
import wget
import getpass


class RegularExpressions:

    def __init__(self):
        #         self.testReverseDateFormatPattern("2020-08-31")
        #         self.testReverseDateFormatPattern("2020-8-31")
        #         self.testReverseDateFormatPattern("2020-8-1")
        #         self.testReverseDateFormatPattern("2020/08/31")
        #         self.testReverseDateFormatPattern("2020/8/31")
        #         self.testReverseDateFormatPattern("2020/8/1")
        #         self.testReverseDateFormatPattern("2020-08-311")
        #         self.testReverseDateFormatPattern("2020-08-aa")
        #         print("---------------------------------------------------")
        #         self.testInternationalPhoneNumberPattern("+52 12 12345678")
        #         self.testInternationalPhoneNumberPattern("+52-12-12345678")
        #         self.testInternationalPhoneNumberPattern("+52 123 1234567")
        #         self.testInternationalPhoneNumberPattern("+52-123-1234567")
        #         self.testInternationalPhoneNumberPattern("+52-12-1234567")
        #         print("---------------------------------------------------")
        #         self.testIPv4AddressPattern("1.1.1.1")
        #         self.testIPv4AddressPattern("12.12.12.12")
        #         self.testIPv4AddressPattern("123.123.123.123")
        #         self.testIPv4AddressPattern("123.123.123.1234")
        #         self.testIPv4AddressPattern("1.1.1")
        #         self.testIPv4AddressPattern("1.1.1.1.1")
        #         print("---------------------------------------------------")
        #         self.testIsInDiccionary("1234")
        #         self.testIsInDiccionary("1234.-")
        #         self.testIsInDiccionary("A1234.-")
        #         print("---------------------------------------------------")
        #         string = """Dormía un león cuando un ratón empezó a juguetear encima de su cuerpo.
        # Despertó el león y lo atrapó. A punto de ser devorado, el ratón le pidió que le perdonara,
        # prometiéndole pagarle en el futuro. El león echó a reír y lo dejó marchar.
        # Días después, unos cazadores apresaron al rey de la selva y lo ataron con una cuerda.
        # Al oír el ratón los lamentos del león, corrió al lugar y royó la cuerda, dejándolo libre.
        # “Días atrás” - le dijo -, “te burlaste de mí pensando que nada podría hacer por ti en agradecimiento.
        # Ahora es bueno que sepas que los pequeños ratones somos agradecidos y cumplidos”.
        # """
        #         self.testSubstituteString(string,"león","SIMBA")
        #         print("---------------------------------------------------")
        #         self.testEmailPattern("a123@aaa.aaa.aaa")
        #         self.testEmailPattern("a.a@aaa.aaa.aaa")
        #         self.testEmailPattern("aa@a.aaa.aaaaaa-aaaaa.a--a.com")
        #         self.testEmailPattern("a-a-aaa123.a.a@a.a.a.com")
        #         self.testEmailPattern("aaaaa-a-aaa123.a.a.@a.a.a.com")
        #         self.testEmailPattern("a-a-aaa123..a...a@a.a.a.com")
        #print("---------------------------------------------------")
        #self.testURLExtractor(r"https://www.ascodevida.com/")

        # Must be run under terminal "py main.py"
        #self.testPasswordStrength()

        # Must be run under terminal "py main.py"
        self.testStrip()

    def testReverseDateFormatPattern(self, strdate):
        # Example valid date format 2020-08-31
        # Example valid date format 2020-8-31
        # Example valid date format 2020-8-1
        # Example valid date format 2020/08/31
        # Example valid date format 2020/8/31
        # Example valid date format 2020/8/1
        regexp = r"^(\d{4}\-\d{1,2}\-\d{1,2})|(\d{4}/\d{1,2}/\d{1,2})$"
        compiled = re.compile(regexp)
        match = compiled.match(strdate)
        search = compiled.search(strdate)
        if search != None:
            group = search.group()
        else:
            group = None
        print("testReverseDateFormatPattern")
        print("str: " + strdate + ", match: " + str(match) + ", search: " + str(search) + ", group: " + str(group))

    def testInternationalPhoneNumberPattern(self, strphone):
        # Example valid number CDMX: +52 12 12345678
        # Example valid number Queretaro: +52-123-1234567
        regexp = r"^\+\d{1,3}(\s|\-)((\d{2}(\s|\-)\d{8})|(\d{3}(\s|\-)\d{7}))$"
        compiled = re.compile(regexp)
        match = compiled.match(strphone)
        search = compiled.search(strphone)
        if search != None:
            group = search.group()
        else:
            group = None
        print("testInternationalPhoneNumberPattern")
        print("str: " + strphone + ", match: " + str(match) + ", search: " + str(search) + ", group: " + str(group))

    def testIPv4AddressPattern(self, stripv4):
        # Example valid IPv address: 1.1.1.1
        # Example valid IPv address: 1.12.12.123
        regexp = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
        compiled = re.compile(regexp)
        match = compiled.match(stripv4)
        search = compiled.search(stripv4)
        if search != None:
            group = search.group()
        else:
            group = None
        print("testIPv4AddressPattern")
        print("str: " + stripv4 + ", match: " + str(match) + ", search: " + str(search) + ", group: " + str(group))

    def testIsInDiccionary(self, string):
        regexp = r"^[\d\.\-]+$"
        compiled = re.compile(regexp)
        match = compiled.match(string)
        search = compiled.search(string)
        if search != None:
            group = search.group()
        else:
            group = None
        print("testIsInDiccionary")
        print("str: " + string + ", match: " + str(match) + ", search: " + str(search) + ", group: " + str(group))

    def testSubstituteString(self, string, stroriginal, strsubstitute):
        compiled = re.compile(stroriginal)
        newstring = compiled.sub(strsubstitute, string)
        print("-----------Original string-----------")
        print(string)
        print("-----------End of String-------------")
        print("\n\n-----------Substituted string-----------")
        if newstring != None:
            print(newstring)
        else:
            print("No substitutions where done.")
        print("-----------End of String-------------")

    def testEmailPattern(self, stremail):
        # Email Rules:

        # Recipient: The recipient name may be a maximum of 64 characters long and consist of:
        # Uppercase and lowercase letters in English (A - Z, a - z)
        # Digits from 0 to 9
        # Special characters such as ! # $ % & ' * + - / = ? ^ _ ' { |
        # A special character cannot appear as the first or last character in an email address or appear
        # consecutively two or more times. The most commonly used special characters are the
        # period(.), underscore(_), hyphen(-) and plus
        # sign(+).

        # Domain Name: The domain name is a string of letters and digits that defines a space on the Internet owned and controlled by a specific mailbox provider or organization.
        # Domain names may be a maximum of 253 characters and consist of:
        # Uppercase and lowercase letters in English (A-Z, a-z)
        # Digits from 0 to 9
        # A hyphen (-)
        # A period (.)  (used to identify a sub-domain; for example,  email.domainsample)

        # Valid email addresses examples
        # a@a.com
        # a123@aaa.aaa.aaa
        # a.a@aaa.aaa.aaa
        # aa@a.aaa.aaaaaa - aaaaa.a - -a.com
        # a-a-aaa123.a.a @ a.a.a.com
        # aaaaa-a-aaa123.a.a. @ a.a.a.com
        # Invalid email addresses examples
        # a-a-aaa123..a...a @ a.a.a.com
        regexp = r"^[\d\w]+([!#\$%&'\*\+\-/=\?\^_'\{\|\.][\d\w]+)*[!#\$%&'\*\+\-/=\?\^_'\{\|\.]?@[\d\w\-]+(\.[\d\w\-]+)+$"
        compiled = re.compile(regexp)
        search = compiled.search(stremail)
        if search != None:
            group = search.group()
        else:
            group = None
        print("testEmailPattern")
        print("str: " + stremail + ", search: " + str(search) + ", group: " + str(group))

    def testURLExtractor(self, url):
        print("URL Extractor")
        print("URL: " + url)
        filename = wget.download(url,"tempfiles/temp.txt")
        print("\nFile Name: " + filename)

        file = open(filename, "r")
        filecontent = file.read()
        file.close()
        regexp = r"https?:\/\/[\w\-]+(\.\w+)+\/([\w-]+\/)*([\w\-]+\.?[\w\-]+)?(\?[\w\-\?=&]+)?"
        compiled = re.compile(regexp)

        urllist = []
        urlfile = open("tempfiles/URLS.txt","a")
        try:
            while len(filecontent) > 0:
                search = compiled.search(filecontent)
                if search != None:
                    print(str(search))
                    group = search.group()
                    #print("group: " + group)
                    newIndex = int(search.span()[1]) + 1
                    urlfile.write(group+"\n")
                    urllist.append(group)
                    filecontent = filecontent[newIndex: len(filecontent)]
                    #print("File Length: "+str(len(filecontent)))
                else:
                    break
            urlfile.close()
        except Exception:
            print("Error ocurred: "+str(Exception))

        for url in urllist:
            self.testURLExtractor(url)

    def calcPasswordStrength(self,strpassword):
        #Password Strength Rules
        #At least 8 characters long.
        #Mixure of uppercase and lowercase letters.
        #Mixure of letters and numbers.
        #At least one special character .,:;-_¡!"#$%&/\()=¿?<>'@{}[]

        MINIMUM_PASSWORD_LENGTH = 8

        strength = 0
        uppercRegexp = r"[A-Z]+"
        lowercRegexp = r"[a-z]+"
        numberRegexp = r"\d+"
        specialRegexp = r"[\.,:;\-_¡!\"#\$%&\/\\(\)=¿\?<>'@{}\[\]\^]"

        print("Password length: " + str(len(strpassword)))
        if len(strpassword) >= MINIMUM_PASSWORD_LENGTH:
            strength += 20
        if re.search(uppercRegexp,strpassword) != None:
            strength += 20
            print("Found upper case characters.")
        if re.search(lowercRegexp,strpassword):
            strength += 20
            print("Found lower case characters.")
        if re.search(numberRegexp,strpassword) != None:
            strength += 20
            print("Found number characters.")
        if re.search(specialRegexp,strpassword) != None:
            print("Found special characters.")
            strength += 20
        return strength

    def testPasswordStrength(self):
        # Must be run under terminal "py main.py"
        while True:
            print("Enter string for password test, quit() to exit: ")
            try:
                password = getpass.getpass()
            except Exception as error:
                print("Error: "+error)
            print("String typed: "+password)
            if(re.search(r"quit\(\)",password)):
                return
            else:
                print("Password strength: "+str(self.calcPasswordStrength(password)))

    # Regex version of strip function.
    def strip(self, string):
        if string == None:
            return None
        elif len(string) > 0:
            search = re.search(r"\S+(\s*\S+)*",string)
            if(search != None):
                return search.group()
        return ""

    def testStrip(self):
        while True:
            string = input("Enter a string chain or quit() to exit: ")
            if string != None:
                if re.search(r"\w*quit\(\)\w*",string):
                    return
                else:
                    string = self.strip(string)
                    print(">"+string+"<")

