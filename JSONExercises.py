import json, yaml, xml.etree.cElementTree as ET, xml
from pprint import pprint as pp

class Company:
    def __init__(self):
        self.name = ""
        self.symbol = ""
        self.industry = ""
        self.field = ""
        self.market_cap = ""
        self.shares_outstanding = ""

    def to_dict(self):
        company_dict = {
            "name" : self.name,
            "symbol" : self.symbol,
            "industry" : self.industry,
            "field" : self.field,
            "market_cap" : self.market_cap,
            "shares_outstanding" : self.shares_outstanding
        }
        return company_dict

    def __str__(self):
        return "Name: " + str(self.name) + ", Symbol: " + str(self.symbol) + ", Industry: " \
               + str(self.industry) + ", Field: " + str(self.field )+ ", Market Cap: " \
               + str(self.market_cap) + ", Shares Outstanding: " + str(self.shares_outstanding)

class Companies:
    def __init__(self):
        self._companies_dict = {}

    def append(self, key, company):
        self._companies_dict[key] = company

    def remove(self, key):
        self._companies_dict.pop(key)

    def to_dict(self):
        dict = {}
        for i in self._companies_dict:
            dict[i] = self._companies_dict[i].to_dict()
        return dict

    def load_from_dict(self, dict):
        for i in dict:
            company = Company()
            company.symbol = i
            company.name = dict[i]["name"]
            company.industry = dict[i]["industry"]
            company.field = dict[i]["field"]
            company.market_cap = dict[i]["market_cap"]
            company.shares_outstanding = dict[i]["shares_outstanding"]
            self._companies_dict[company.symbol] = company

    def __str__(self):
        string = ""
        for i in self._companies_dict:
            string += str(self._companies_dict[i])+"\n"
        return string


def dict_to_xml(value, title):
    return "<?xml version =\"1.0\"?>\n<"+title+">\n"+dict_to_xml_recursive(value)+"\n</"+title+">"

def dict_to_xml_recursive(value):
    xml_text = ""
    for k, v in value.items():
        xml_text += "\n" + "<"+str(k)+">"
        if isinstance(v, dict):
            xml_text += dict_to_xml_recursive(value[k])
        else:
            xml_text += value[k]
        xml_text += "</" + str(k) + ">"
    return xml_text

def xml_to_dict(value):
    tree = ET.fromstring(value)
    return xml_to_dict_recursive(tree)

def xml_to_dict_recursive(tree):
    xml_dict = {}
    for i in tree.getchildren():
        c = i.getchildren()
        if len(c) > 0:
            xml_dict[i.tag] = xml_to_dict_recursive(i)
        else:
            xml_dict[i.tag] = i.text
    return xml_dict



def main():

    JSON_FILE_NAME = "tempfiles\\Companies_File.json"
    YAML_FILE_NAME = "tempfiles\\Companies_File.yaml"
    XML_FILE_NAME = "tempfiles\\Companies_File.xml"

    # msft_dict = {
    #     "name" : "Microsoft",
    #     "symbol" : "MSFT",
    #     "industry" : "Technology",
    #     "field" : "Software - Infrastructure",
    #     "market_cap" : "1635000000000",
    #     "shares_outstanding" : "7580000000"
    # }
    #
    # adbe_dict = {
    #     "name" : "Adobe",
    #     "symbol" : "ADBE",
    #     "industry" : "Technology",
    #     "field" : "Software - Infrastructure",
    #     "market_cap" : "231990000000",
    #     "shares_outstanding" : "480000000"
    # }
    #
    # orcl_dict = {
    #     "name" : "Oracle",
    #     "symbol" : "ORCL",
    #     "industry" : "Technology",
    #     "field" : "Software - Infrastructure",
    #     "market_cap" : "180352000000",
    #     "shares_outstanding" : "3040000000"
    # }
    #
    # sq_dict = {
    #     "name" : "Square Inc.",
    #     "symbol" : "sq",
    #     "industry" : "Technology",
    #     "field" : "Software - Infrastructure",
    #     "market_cap" : "78030000000",
    #     "shares_outstanding" : "440120000000"
    # }

    msft = Company()
    msft.name = "Microsoft"
    msft.symbol = "MSFT"
    msft.industry = "Technology"
    msft.field = "Software - Infrastructure"
    msft.market_cap = "1635000000000"
    msft.shares_outstanding = "7580000000"

    adbe = Company()
    adbe.name = "Adobe"
    adbe.symbol = "ADBE"
    adbe.industry = "Technology"
    adbe.field = "Software - Infrastructure"
    adbe.market_cap = "231990000000"
    adbe.shares_outstanding = "480000000"

    orcl = Company()
    orcl.name = "Oracle"
    orcl.symbol = "ORCL"
    orcl.industry = "Technology"
    orcl.field = "Software - Infrastructure"
    orcl.market_cap = "180352000000"
    orcl.shares_outstanding  = "3040000000"

    sq = Company()
    sq.name = "Square Inc."
    sq.symbol = "SQ"
    sq.industry = "Technology"
    sq.field = "Software - Infrastructure"
    sq.market_cap = "78030000000"
    sq.shares_outstanding = "440120000000"

    companies = Companies()
    companies.append(msft.symbol, msft)
    companies.append(adbe.symbol, adbe)
    companies.append(orcl.symbol, orcl)
    companies.append(sq.symbol, sq)
    ##############################################################

    print("Company Objects")
    print(companies)

    print("Company_dict:")
    companies_dict = companies.to_dict()
    pp(companies_dict)

    ##############################################################3
    print("\nEncoding Python Objects into JSON:")
    json_encode = json.dumps(companies_dict)
    print("\nJSON Encoded")
    pp(json_encode)

    print("Writing on file:" + JSON_FILE_NAME)
    with open(JSON_FILE_NAME, "w") as f:
        f.write(json_encode)

    print("Reading from file:" + JSON_FILE_NAME)
    with open(JSON_FILE_NAME, "r") as f:
        text = f.read()

    print("\nFile Content: ")
    pp(text)
    print("\nDecoding from JSON: ")
    decode_dict = json.loads(text)
    pp(decode_dict)

    print("Converted to Objects")
    companies = Companies()
    companies.load_from_dict(decode_dict)
    print(companies)


    ##############################################################3
    print("Encoding Python Objects into Yaml")
    yaml_encode = yaml.dump(companies.to_dict())
    pp(yaml_encode)

    with open(YAML_FILE_NAME,"w") as f:
        f.write(yaml_encode)


    print("Reading from file:" + YAML_FILE_NAME)
    with open(YAML_FILE_NAME,"r") as f:
        text = f.read()

    print("File content:")
    pp(text)
    decode_dict = yaml.load(text, Loader=yaml.FullLoader)
    print("Decoding from Yaml")
    pp(decode_dict)

    print("Converted to Objects")
    companies = Companies()
    companies.load_from_dict(decode_dict)
    print(companies)


    ##############################################################3
    print("Encoding Python Objects into XML")
    xml_encode = dict_to_xml(companies.to_dict(),"companies")
    pp(xml_encode)

    with open(XML_FILE_NAME, "w") as f:
        f.write(xml_encode)


    print("Reading from file: "+XML_FILE_NAME)
    with open(XML_FILE_NAME,"r") as f:
        text = f.read()
    print("File content:")
    pp(text)

    print("Converted to Objects")
    decode_dict = xml_to_dict(text)
    pp(decode_dict)

    companies = Companies()
    companies.load_from_dict(decode_dict)
    print(companies)