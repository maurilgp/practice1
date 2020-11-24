#Maurilio Gonzalez Paz

import pandas, datetime, yfinance, os, numpy
from pprint import pprint as pp
import  matplotlib.pyplot as plt


def extract_columns(array, columns):
    array2 = []
    for row in array:
        array_row = []
        for c in columns:
            print(str(c)+"\t"+str(row[c])+str(type(row[c])))
            array_row.append(row[c])
        array2.append(array_row)
    return pandas.DataFrame(array2)


def main():
    print("Principal Component Analysis on Stock Market")
    sp500_list = ["A", "AAL", "AAP", "AAPL", "ABBV", "ABC", "ABMD", "ABT", "ACN", "ADBE", "ADI", "ADM",
              "ADP", "ADSK", "AEE", "AEP", "AES", "AFL", "AIG", "AIV", "AIZ", "AJG", "AKAM", "ALB",
              "ALGN", "ALK", "ALL", "ALLE", "ALXN", "AMAT", "AMCR", "AMD", "AME", "AMGN", "AMP",
              "AMT", "AMZN", "ANET", "ANSS", "ANTM", "AON", "AOS", "APA", "APD", "APH", "APTV", "ARE",
              "ATO", "ATVI", "AVB", "AVGO", "AVY", "AWK", "AXP", "AZO", "BA", "BAC", "BAX", "BBY",
              "BDX", "BEN", "BF.B", "BIIB", "BIO", "BK", "BKNG", "BKR", "BLK", "BLL", "BMY", "BR",
              "BRK.B", "BSX", "BWA", "BXP", "C", "CAG", "CAH", "CARR", "CAT", "CB", "CBOE", "CBRE",
              "CCI", "CCL", "CDNS", "CDW", "CE", "CERN", "CF", "CFG", "CHD", "CHRW", "CHTR", "CI",
              "CINF", "CL", "CLX", "CMA", "CMCSA", "CME", "CMG", "CMI", "CMS", "CNC", "CNP", "COF",
              "COG", "COO", "COP", "COST", "CPB", "CPRT", "CRM", "CSCO", "CSX", "CTAS", "CTLT",
              "CTSH", "CTVA", "CTXS", "CVS", "CVX", "CXO", "D", "DAL", "DD", "DE", "DFS", "DG",
              "DGX", "DHI", "DHR", "DIS", "DISCA", "DISCK", "DISH", "DLR", "DLTR", "DOV", "DOW",
              "DPZ", "DRE", "DRI", "DTE", "DUK", "DVA", "DVN", "DXC", "DXCM", "EA", "EBAY", "ECL",
              "ED", "EFX", "EIX", "EL", "EMN", "EMR", "EOG", "EQIX", "EQR", "ES", "ESS", "ETN", "ETR",
              "ETSY", "EVRG", "EW", "EXC", "EXPD", "EXPE", "EXR", "F", "FANG", "FAST", "FB", "FBHS",
              "FCX", "FDX", "FE", "FFIV", "FIS", "FISV", "FITB", "FLIR", "FLS", "FLT", "FMC", "FOX",
              "FOXA", "FRC", "FRT", "FTI", "FTNT", "FTV", "GD", "GE", "GILD", "GIS", "GL", "GLW",
              "GM", "GOOG", "GOOGL", "GPC", "GPN", "GPS", "GRMN", "GS", "GWW", "HAL", "HAS", "HBAN",
              "HBI", "HCA", "HD", "HES", "HFC", "HIG", "HII", "HLT", "HOLX", "HON", "HPE", "HPQ",
              "HRL", "HSIC", "HST", "HSY", "HUM", "HWM", "IBM", "ICE", "IDXX", "IEX", "IFF", "ILMN",
              "INCY", "INFO", "INTC", "INTU", "IP", "IPG", "IPGP", "IQV", "IR", "IRM", "ISRG", "IT",
              "ITW", "IVZ", "J", "JBHT", "JCI", "JKHY", "JNJ", "JNPR", "JPM", "K", "KEY", "KEYS",
              "KHC", "KIM", "KLAC", "KMB", "KMI", "KMX", "KO", "KR", "KSU", "L", "LB", "LDOS", "LEG",
              "LEN", "LH", "LHX", "LIN", "LKQ", "LLY", "LMT", "LNC", "LNT", "LOW", "LRCX", "LUMN",
              "LUV", "LVS", "LW", "LYB", "LYV", "MA", "MAA", "MAR", "MAS", "MCD", "MCHP", "MCK",
              "MCO", "MDLZ", "MDT", "MET", "MGM", "MHK", "MKC", "MKTX", "MLM", "MMC", "MMM", "MNST",
              "MO", "MOS", "MPC", "MRK", "MRO", "MS", "MSCI", "MSFT", "MSI", "MTB", "MTD", "MU",
              "MXIM", "NCLH", "NDAQ", "NEE", "NEM", "NFLX", "NI", "NKE", "NLOK", "NLSN", "NOC", "NOV",
              "NOW", "NRG", "NSC", "NTAP", "NTRS", "NUE", "NVDA", "NVR", "NWL", "NWS", "NWSA", "O",
              "ODFL", "OKE", "OMC", "ORCL", "ORLY", "OTIS", "OXY", "PAYC", "PAYX", "PBCT", "PCAR",
              "PEAK", "PEG", "PEP", "PFE", "PFG", "PG", "PGR", "PH", "PHM", "PKG", "PKI", "PLD", "PM",
              "PNC", "PNR", "PNW", "POOL", "PPG", "PPL", "PRGO", "PRU", "PSA", "PSX", "PVH", "PWR",
              "PXD", "PYPL", "QCOM", "QRVO", "RCL", "RE", "REG", "REGN", "RF", "RHI", "RJF", "RL",
              "RMD", "ROK", "ROL", "ROP", "ROST", "RSG", "RTX", "SBAC", "SBUX", "SCHW", "SEE", "SHW",
              "SIVB", "SJM", "SLB", "SLG", "SNA", "SNPS", "SO", "SPG", "SPGI", "SRE", "STE", "STT",
              "STX", "STZ", "SWK", "SWKS", "SYF", "SYK", "SYY", "T", "TAP", "TDG", "TDY", "TEL",
              "TER", "TFC", "TFX", "TGT", "TIF", "TJX", "TMO", "TMUS", "TPR", "TROW", "TRV", "TSCO",
              "TSN", "TT", "TTWO", "TWTR", "TXN", "TXT", "TYL", "UA", "UAA", "UAL", "UDR", "UHS",
              "ULTA", "UNH", "UNM", "UNP", "UPS", "URI", "USB", "V", "VAR", "VFC", "VIAC", "VLO",
              "VMC", "VNO", "VNT", "VRSK", "VRSN", "VRTX", "VTR", "VTRS", "VZ", "WAB", "WAT", "WBA",
              "WDC", "WEC", "WELL", "WFC", "WHR", "WLTW", "WM", "WMB", "WMT", "WRB", "WRK", "WST", "WU",
              "WY", "WYNN", "XEL", "XLNX", "XOM", "XRAY", "XRX", "XYL", "YUM", "ZBH", "ZBRA", "ZION",
              "ZTS"]

    file_path = os.path.abspath("../tempfiles/StockMarketPCA.xlsx")

    if not os.path.exists(file_path):
        start_date = "2020-01-01"
        end_date = str(datetime.date.today())
        period = "1d"

        print("Downloading data of the following list")
        pp(sp500_list)
        print("Start Date: "+start_date)
        print("End Date: "+end_date)
        print("Period: "+period)

        ticker_df = pandas.DataFrame()
        for company_symbol in sp500_list:
            company_ticker = yfinance.Ticker(company_symbol)
            print("Attempting to download data: "+company_symbol)
            company_history = company_ticker.history(start=start_date, end=end_date, period=period)
            with pandas.ExcelWriter(file_path) as wr:
                ticker_df[company_symbol] = company_history["Close"]
                print("Attempting to save data: "+company_symbol)
                ticker_df.to_excel(excel_writer=wr, sheet_name="SP500")

    ticker_df = pandas.read_excel(file_path)
    ticker_df = ticker_df.fillna(0)
    print("Columns found:")
    print(ticker_df.columns)
    del ticker_df["Unnamed: 0"]

    ticker_df.apply(pandas.to_numeric)
    print(ticker_df["VNT"])

    print("Company historic stock prices:")
    pp(ticker_df)

    ticker_mean = ticker_df.mean()
    print("Company stock prices mean:")
    print(ticker_mean)

    ticker_centered = ticker_df - ticker_mean
    print("Mean centered data:")
    print(ticker_centered)

    ticker_covariance = ticker_centered.cov()
    print("Covariance")
    print(ticker_covariance)

    ticker_eigenvalues, ticker_eigenvectors = numpy.linalg.eig(ticker_covariance)


    print("Eigenvalues")
    print(ticker_eigenvalues)

    ticker_eigenvalues_var = ticker_eigenvalues / sum(ticker_eigenvalues) * 100
    print("Eigenvalues Variance")
    print(ticker_eigenvalues_var)

    print("Eigen Vectors")
    print(ticker_eigenvectors)

    print("Projected")
    projected = ticker_eigenvectors.T.dot(ticker_centered.T)
    pp(projected.T)

    extracted_df = extract_columns(projected.T, [0,1])
    print(extracted_df)

    fig, ax = plt.subplots()
    fig.suptitle("SP500 Companies")
    ax.scatter(extracted_df[0], extracted_df[1])
    for i, txt in enumerate(sp500_list):
        print(str(txt)+"\t"+str(extracted_df[0][i])+"\t"+str(extracted_df[1][i]))
        ax.annotate(txt, extracted_df[0][i], extracted_df[1][i])
    plt.show()




if __name__ == "__main__":
    main()
