#Read an Afluenta File and perform some statistics.

import os, logging, openpyxl, datetime, sys, pandas, pprint

class Loan:
    ID = "ID"
    LTYPE = "LOAN TYPE"
    DATE = "ACQUIRED DATE"
    DESTINATION = "LOAN DESTINATION"
    AGE = "LOANER AGE"
    EARNINGS = "EARNINGS"
    ACTIVITY = "ECONOMICAL ACTIVITY"
    GEOGRAPHICZONE = "GEOGRAPHIC ZONE"
    PROFILE = "PROFILE"
    AMOUNT = "AMOUNT"
    APR = "APR"
    TERM = "TERM"
    SHARE = "SHARE"
    INTEREST = "INTEREST"
    INVESTINGSYSTEM = "INVESTING SYSTEM"
    BIDTYPE = "BID TYPE"
    STATUS = "STATUS"


class LoanDatabase:
    def __init__(self):
        self._FILEPATH = os.path.abspath("tempfiles\\LenderLoansSummary.xlsx")
        self._loan_list = []
        self.load_database()
        self.load_database2()


    def load_database(self):
        logging.debug("Attempting to load: " + self._FILEPATH)
        loan_entry = {}
        try:
            wb = openpyxl.load_workbook(self._FILEPATH)
            sn = wb.get_sheet_names()
            logging.debug("Spreadsheets found: " + str(sn))
            ws = wb.get_sheet_by_name(sn[0])
            rows = tuple(ws.rows)
            first_row = True
            for r in rows:
                if first_row:
                    first_row = False
                else:
                    if r[1].value is not None:
                        loan_entry[Loan.ID] = r[1].value
                        loan_entry[Loan.LTYPE] = r[2].value
                        loan_entry[Loan.DATE] = r[3].value
                        loan_entry[Loan.DESTINATION] = r[4].value
                        loan_entry[Loan.AGE] = r[5].value
                        loan_entry[Loan.EARNINGS] = r[6].value
                        loan_entry[Loan.ACTIVITY] = r[7].value
                        loan_entry[Loan.GEOGRAPHICZONE] = r[8].value
                        loan_entry[Loan.PROFILE] = r[9].value
                        loan_entry[Loan.AMOUNT] = r[10].value
                        loan_entry[Loan.APR] = r[11].value
                        loan_entry[Loan.TERM] = r[12].value
                        loan_entry[Loan.SHARE] = r[13].value
                        loan_entry[Loan.INTEREST] = r[14].value
                        loan_entry[Loan.INVESTINGSYSTEM] = r[15].value
                        loan_entry[Loan.BIDTYPE] = r[16].value
                        loan_entry[Loan.STATUS] = r[17].value
                        self._loan_list.append(loan_entry)
                        logging.debug("Afluenta Loan loaded successfully.")
            loan_dataframe = pandas.DataFrame(self._loan_list)
            print(loan_dataframe)
        except Exception:
            logging.debug("Error occurred while opening Excel file: " + self._FILEPATH)
            logging.debug("Unexpected error: ", sys.exc_info()[0])

    def load_database2(self):
        loan_dataframe = pandas.read_excel(self._FILEPATH, index_col="ID")
        #loan_dataframe[loan_dataframe == ""] = "No aplica"
        #loan_dataframe.fillna = "No definido"
        #pandas.set_option("display.max_rows",loan_dataframe.shape[0]+1)
        print("\nData Frame:")
        print(loan_dataframe)
        print("\nColumns:")
        print(loan_dataframe.columns)
        print("\nCount individual columns.")
        for i in loan_dataframe.columns:
            print("\n###################################################################")
            print("\n"+str(i))
            counts = loan_dataframe[i].value_counts()
            pprint.pprint(counts)
            print("Dataset Size: "+str(len(counts)))


        print("\nCount by groups.")

        columns = pandas.Series(loan_dataframe["Cuota"])
        print(columns)

        for i in loan_dataframe.columns:
            for j in loan_dataframe.columns:
                if i != j:
                    print("Count grouping "+str(i)+" with "+str(j))
                    columns = pandas.Series(loan_dataframe[j])
                    grouped = loan_dataframe.groupby(i, columns)
                    counts = grouped.size().unstack().fillna(0)
                    pprint.pprint(counts)

