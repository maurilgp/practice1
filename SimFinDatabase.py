import simfin

class SimFinDatabase:
    def __init__(self):
        # Set your API-key for downloading data. This key gets the free data.
        simfin.set_api_key('free')

        # Set the local directory where data-files are stored.
        # The directory will be created if it does not already exist.
        simfin.set_data_dir('~/simfin_data/')

        # Download the data from the SimFin server and load into a Pandas DataFrame.
        df = simfin.load_companies(market='us')

        # Print the first rows of the data.
        print(df.head())


        simfin.load_companies(market='us')