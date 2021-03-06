import pandas, datetime, yfinance, os
from pprint import pprint as pp

def main():
    company_symbol = "IBM"
    print("Yahoo Finance Data Extraction Example")

    today = datetime.date.today()

    ibm = yfinance.Ticker(company_symbol)
    print(company_symbol)
    print("------------------------------------------------------")
    print("Stock Info")
    print("------------------------------------------------------")
    pp(ibm.info)
    print("------------------------------------------------------")
    print("Dividends")
    print("------------------------------------------------------")
    pp(ibm.dividends)
    print("------------------------------------------------------")
    print("Split")
    print("------------------------------------------------------")
    pp(ibm.splits)
    print("------------------------------------------------------")
    print("Financials")
    print("------------------------------------------------------")
    pp(ibm.financials)
    print("------------------------------------------------------")
    print("Quaterly Financials")
    print("------------------------------------------------------")
    print("------------------------------------------------------")
    pp(ibm.quarterly_financials)
    print("Mayor Holders")
    print("------------------------------------------------------")
    pp(ibm.major_holders)
    print("------------------------------------------------------")
    print("Institutional Holders")
    print("------------------------------------------------------")
    pp(ibm.institutional_holders)
    print("------------------------------------------------------")
    print("Balance Sheet")
    print("------------------------------------------------------")
    pp(ibm.balance_sheet)
    print("------------------------------------------------------")
    print("Cash Flow")
    print("------------------------------------------------------")
    pp(ibm.cashflow)
    print("------------------------------------------------------")
    print("Earnings")
    print("------------------------------------------------------")
    pp(ibm.earnings)
    print("------------------------------------------------------")
    print("Sustainability")
    print("------------------------------------------------------")
    pp(ibm.sustainability)
    print("------------------------------------------------------")
    print("Recommendations")
    print("------------------------------------------------------")
    pp(ibm.recommendations)
    print("------------------------------------------------------")
    print("Calendar")
    print("------------------------------------------------------")
    pp(ibm.calendar)
    print("------------------------------------------------------")
    print("ISIN")
    print("------------------------------------------------------")
    pp(ibm.isin)
    print("------------------------------------------------------")
    print("Options")
    print("------------------------------------------------------")
    pp(ibm.options)
    print("------------------------------------------------------")
    print("Options Chains")
    print("------------------------------------------------------")
    pp(ibm.option_chain("2023-01-20"))
    print("------------------------------------------------------")
    print("History")
    print("------------------------------------------------------")
    ibm_stocks = ibm.history(start="2020-01-01", end=str(datetime.date.today()), period="1d")
    pp(ibm_stocks)

    ibm_close = ibm_stocks["Close"]
    pp(ibm_close)
    print("ibm_close: "+str(type(ibm_close)))
    df = pandas.DataFrame()
    df[company_symbol] = ibm_close
    print("------------------------------------------------------")
    print("Data Frame")
    print("------------------------------------------------------")
    pp(df)

    PATH = os.path.abspath("../tempfiles/YahooFinance.xlsx")
    with pandas.ExcelWriter(PATH) as wr:
        df.to_excel(wr, sheet_name=company_symbol)

if __name__ == "__main__":
    main()