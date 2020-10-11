import os, logging, sys, json, pprint, collections, pandas, matplotlib, re


class PhytonForDataAnalysis_ch02:
    def __init__(self):
        PATH = os.path.abspath("tempfiles\\bitly_usagov\\example.txt")
        logging.debug("Attempting to load file: "+PATH)
        try:
            line = open(PATH).readline()
            logging.debug("File loaded successfully!")
            pprint.pprint(line)

            print("\nRecords as dictionary created by parsing python")
            records = [json.loads(line) for line in open(PATH)]
            pprint.pprint(records[0])

            print("\nTime Zones found in JSON file.")
            time_zones = [rec["tz"] for rec in records if "tz" in rec]
            count_time_zones = self.get_counts(time_zones)
            pprint.pprint(count_time_zones)
            print("\nCount Time Zones.")
            top_counts_time_zones = self.get_top_counts(count_time_zones,10)
            print("\nTop 10 Time Zones manual calculated.")
            pprint.pprint(top_counts_time_zones)

            count_time_zones = collections.Counter(time_zones)
            top_counts_time_zones = count_time_zones.most_common(10)
            print("\nTop 10 Time Zones from collections library.")
            pprint.pprint(top_counts_time_zones)



            print("\nNow with pandas.")
            frame = pandas.DataFrame(records)
            print(frame)
            time_zones_frame = frame["tz"]
            time_zones_frame = time_zones_frame.fillna("Missing")
            time_zones_frame[time_zones_frame == ""] = "Unknown"
            count_time_zones_frame = time_zones_frame.value_counts()
            top_counts_time_zones_frame = count_time_zones_frame[:10]
            print("\nTop time zones.")
            pprint.pprint(top_counts_time_zones_frame)
            #top_counts_time_zones_frame.plot(kind="barh", rot=0)
            #matplotlib.pyplot.show()


            browsers_frame = pandas.Series([x.split()[0] for x in frame["a"].dropna()])
            print("\nBrowsers.")
            pprint.pprint(browsers_frame)
            count_browsers_frame = browsers_frame.value_counts()
            print("\nTop Browsers.")
            pprint.pprint(count_browsers_frame[:10])


            print("\nOperating Systems.")
            operating_systems = []
            regex_exp = r"\(\w+"
            compiled = re.compile(regex_exp)
            for x in frame["a"].dropna():
                search = compiled.search(x)
                if search is not None:
                    operating_sys = search.group()
                    operating_sys = operating_sys[1:len(operating_sys)]
                    operating_systems.append(operating_sys)

            operating_systems = pandas.Series(operating_systems)
            pprint.pprint(operating_systems)

            print("\nTop Operating Systems.")
            count_operating_systems = operating_systems.value_counts()
            pprint.pprint(count_operating_systems[:10])


            print("Time Zone by Operating System.")
            cframe = frame[frame["a"].notnull()]
            timezone_and_os = cframe.groupby(["tz", operating_systems])
            count_timezone_and_os = timezone_and_os.size().unstack().fillna(0)
            pprint.pprint(count_timezone_and_os)
            indexer = count_timezone_and_os.sum(1).argsort()
            pprint.pprint(indexer[:10])
            #time_zone_and_operating_system =



        except Exception:
            logging.debug("Error opening file: "+PATH)
            print(sys.exc_info()[0])


    def get_counts(self, sequence):
        counts = {}
        for i in sequence:
            if i in counts:
                counts[i] += 1
            else:
                counts[i] = 1
        return counts

    def get_top_counts(self, counts, top):
        value_key_pairs = [(count, item) for item,count in counts.items()]
        value_key_pairs.sort()
        return value_key_pairs[-top:]
