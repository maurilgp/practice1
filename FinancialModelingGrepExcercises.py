import requests, json, os

class FinancialModelingGrep:
    def __init__(self):
        pass


def main():
    SITE = "https://financialmodelingprep.com/api/v3/profile/"
    COMPANY_TICKER = "AAPL"
    MY_API_KEY = "9ea94cf0bb1827dd9cf69e84fab76be1"

    FILE_NAME = os.path.abspath("tempfiles\\"+COMPANY_TICKER+".json")

    url = SITE+COMPANY_TICKER+"?apikey="+MY_API_KEY
    print("Query data from URL: "+url)

    response = requests.get(url)
    print("----------------------------------")
    print(response)
    print("----------------------------------")
    content = response.content
    print()
    print("----------------------------------")
    json = response.json()
    print(json)

    with open(file=FILE_NAME, mode="w") as f:
        f.write(str(json))



