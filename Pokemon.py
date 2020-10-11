#Pandas Dataframe excersices using a pokemon database.
import pandas, re, pprint, os, logging

class Pokemon:
    def __init__(self):
        self.pokemon()
        #self.exercise1()
        #self.exercise2()
        #self.exercise3()

    def _increment(self, base, ben, pos=0):
        if pos == len(ben):
            ben.append(0)
        elif ben[pos] + 1 == base:
            ben[pos] = 0
            self._increment(base=base, ben=ben, pos=pos + 1)
        else:
            ben[pos] += 1
        return ben

    def _little_endian_number(self, value, base):
        ben = [0]
        for i in range(value):
            ben = self._increment(base=base, ben=ben)
            #logging.debug(str(i)+"\t"+str(ben))
        ben.reverse()
        #logging.debug("Number: " + str(value) + "\tLittle Endian Number: " + str(ben))
        return ben

    def _decimal_to_alphabet(self, value):
        FIRST_CHARACTER = 65
        MAX_BASE_NUMBER = 26
        lnumber = self._little_endian_number(value=value, base=MAX_BASE_NUMBER)
        alphabet = ""
        for i in lnumber:
            alphabet += chr(FIRST_CHARACTER+i)
        #logging.debug("Little Endian Number: "+str(little_endian_number)+"\tAlphabet Number: "+alphabet)
        return alphabet

    def _generate_column_names(self, size):
        column_names = []
        for i in range(size):
            alphabet = self._decimal_to_alphabet(i)
            column_names.append(alphabet)
        logging.debug("Column Names: "+str(column_names))
        return column_names

    def pokemon(self):
        pokemon_dataframe = pandas.read_csv(os.path.abspath("tempfiles\\pokemon_data.csv"))

        # Clean dataframe
        pokemon_dataframe = pokemon_dataframe.fillna("No value")

        print("\nPokemon Dataset:")
        pprint.pprint(pokemon_dataframe)
        columns = pokemon_dataframe.columns
        print("\nPokemon Dataset Columns found:")
        pprint.pprint(columns)

        print("\nPrint specific columns:")
        pprint.pprint(pokemon_dataframe[["Name", "Type 1", "Generation"]])

        print("\nPrint single row:")
        pprint.pprint(pokemon_dataframe.iloc[0])

        print("\nPrint specific rows:")
        pprint.pprint(pokemon_dataframe.iloc[0:5])

        print("\nPrint specific location:")
        print(pokemon_dataframe.iloc[2, 1])

        print("\nPerform a query:")
        query_dataframe = pokemon_dataframe.loc[pokemon_dataframe["Type 1"] == "Fire"]
        query_dataframe = query_dataframe.loc[query_dataframe["Type 2"] == "Ground"]
        pprint.pprint(query_dataframe)

        print("\nBasic statistics")
        pprint.pprint(pokemon_dataframe.describe())

        print("\nSort by Name Descending and print the first 20:")
        pprint.pprint(pokemon_dataframe.sort_values(["Attack", "Defense"], ascending=False).iloc[0:20])

        print("\nAdding new data:")
        pokemon_dataframe["Total Score"] = pokemon_dataframe["HP"] + pokemon_dataframe["Attack"] + \
                                           pokemon_dataframe["Defense"] + pokemon_dataframe["Sp. Atk"] + \
                                           pokemon_dataframe["Sp. Def"] + pokemon_dataframe["Speed"]
        pokemon_dataframe = pokemon_dataframe[pokemon_dataframe["Total Score"] > 500]
        pprint.pprint(pokemon_dataframe.head(20))

        print("\nDeleting columns:")
        pokemon_dataframe2 = pokemon_dataframe.drop(columns=["Generation", "Legendary"])
        pprint.pprint(pokemon_dataframe2.head(20))

        print("\nChanging column order:")
        pokemon_dataframe2 = pokemon_dataframe2[
            ["Name", "Type 1", "Type 2", "HP", "Attack", "Sp. Atk", "Defense", "Sp. Def", "Speed", "Total Score"]]
        pprint.pprint(pokemon_dataframe2.head(20))

        print("\nConvert to excel:")
        pokemon_dataframe2.to_excel(os.path.abspath("tempfiles\\pokemon_dataframe2.xlsx"))

        writer = pandas.ExcelWriter(os.path.abspath("tempfiles\\pokemons_by_type.xlsx"))
        print("\nSeparate type pokemons:")
        type_series = pandas.Series(pokemon_dataframe["Type 1"])
        count_type_series = type_series.value_counts()
        pprint.pprint(count_type_series)
        pandas.DataFrame(count_type_series).to_excel(writer, sheet_name="statistics")
        for k, v in count_type_series.items():
            print("#########################################")
            print(k)
            type_dataframe = pokemon_dataframe[pokemon_dataframe["Type 1"] == k]
            pprint.pprint(type_dataframe)
            type_dataframe.to_excel(writer, sheet_name=str(k))
        writer.save()

    def exercise1(self):
        a = pandas.DataFrame({"Dataframe:A Column:A": [i for i in range(10)]})
        b = pandas.DataFrame({"Dataframe:B Column:A": [i for i in range(10)]})
        print("###################################################################3")
        print("Exercise 1: Join two Data frames.")

        print("====================================")
        print("a dataframe")
        pprint.pprint(a["Dataframe:A Column:A"])
        print("a series")
        aseries = pandas.Series(a["Dataframe:A Column:A"])
        pprint.pprint(aseries)

        print("====================================")
        print("b dataframe")
        pprint.pprint(b["Dataframe:B Column:A"])
        print("b series")
        bseries = pandas.Series(b["Dataframe:B Column:A"])
        pprint.pprint(bseries)


        print("====================================")
        print("Joining two series")
        c = pandas.DataFrame({a.columns[0]: aseries, b.columns[0]: bseries})
        pprint.pprint(c)
        print("====================================")
        print("Joining two dataframe columns")
        d = pandas.DataFrame()
        d[a.columns[0]] = a[a.columns[0]]
        d[b.columns[0]] = b[b.columns[0]]
        pprint.pprint(d)

    def exercise2(self):
        columns = 100
        rows = 1000

        columns_name = self._generate_column_names(size=columns)
        rows_name = ["row" + str(i) for i in range(rows)]
        data_dictionary = {}
        i=0
        for cn in columns_name:
            rdata = []
            for j in range(rows):
                rdata.append(i*j)
            data_dictionary[cn] = rdata
            i += 1

        df = pandas.DataFrame(data_dictionary, index=rows_name)
        print("###################################################################3")
        print("Exercise 2: Generate a Data Frame")
        pprint.pprint(df)
        df2 = df[df["B"] > 100]
        df2 = df2[df2["B"] < 200]
        pprint.pprint(df2)


    def exercise3(self):
        dictionary = {}
        size = 20
        for i in range(size):
            data = []
            for j in range(size):
                data.append(i+j)
            dictionary[self._decimal_to_alphabet(i)] = data
        print("Dictionary: ")
        pprint.pprint(dictionary)
        print("Data Frame: ")
        df = pandas.DataFrame(dictionary)
        print("###################################################################3")
        print("Exercise 3: Data Frame")
        pprint.pprint(df)
        sc = pandas.DataFrame()
        sc["Sum Columns"] = [0] * len(df.columns)
        sr_dict = {}
        for c in df.columns:
            sc["Sum Columns"] += df[c]
            sr_dict[c] = 0
            for v in df[c]:
                sr_dict[c] += v
        pprint.pprint(sr_dict)
        df[sc.columns[0]] = sc[sc.columns[0]]
        print("Adding column values:")
        pprint.pprint(df)
        df = df.append(sr_dict, ignore_index=True)
        print("Adding row values:")
        pprint.pprint(df)

