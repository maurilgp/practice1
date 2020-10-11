import requests, logging, re, pprint, sys

class WebDownloaer():
    def __init__(self):
        self.LOGGING_FILE = "tempfiles\\WEBDOWNLOADER.LOG"
        self.URL_FILE = "tempfiles\\URL_FILE.TXT"
        self.BLACKLIST_URL_FILE = "tempfiles\\BLACKLIST_URL_FILE.TXT"
        self.url_db = []
        self.blacklist_url_db = []

        self.initialize_logging()
        logging.debug("-----------Begin of program WebDownloader------------")
        self.initialize_urldb()
        self.initialize_blacklist_urldb()
        #strurl = "http://www.gutenberg.org/cache/epub/4693/pg4693.txt"
        strurl="https://en.wikipedia.org/wikiSuper_Mario_All-Stars"
        self.explore_web(strurl)
        logging.debug("-----------End of program WebDownloader------------")

    def explore_web(self, strurl):
        request_attempts = 0
        max_request_attempts = 3
        while True:
            request_attempts += 1
            if request_attempts < max_request_attempts:
                logging.debug("Attempt "+str(request_attempts)+" to download the URL: " + strurl)
                try:
                    req = requests.get(strurl)
                    if req.status_code == requests.codes.ok:
                        logging.debug("URL downloaded successfully. File length: "+str(len(req.text))+" bytes")
                        urls = self.geturls(req.text)
                        logging.debug("URLs found in document: "+str(urls))
                        for u in urls:
                            if not u in self.url_db and not u in self.blacklist_url_db:
                                logging.debug("Found a new url: "+u+" saving to database.")
                                self.update_urldb(u)
                                self.explore_web(u)
                    else:
                        logging.debug("Error occurred while trying to download URL: "+urls)
                        continue
                except Exception:
                    logging.error("Error downloading the URL: "+strurl)
                    logging.error(str(sys.exc_info()[0]))
                    return
            else:
                logging.error("Maximum attempts reached for URL: "+strurl)
                self.update_blacklist_urldb(strurl)
                return

    def geturls(self, string):
        urls = []
        pattern = r"https?:\/\/[\w\d\-_]+(\.[\w\d\-_]+)*(\/[\w\d\-_\?=\+&\.%:]*)*"
        compiled = re.compile(pattern)
        while True:
            if len(string) > 0:
                search = compiled.search(string)
                if search != None:
                    urlstr = search.group()
                    urls.append(urlstr)
                    string = string[search.span()[1]: len(string)]
                else:
                    break
        return urls

    def update_urldb(self, strurl):
        self.url_db.append(strurl)
        try:
            with open(self.URL_FILE,"a") as f:
                f.write(strurl+"\n")
                logging.debug("Adding URL: "+str(strurl)+" to database.")
        except:
            logging.error("Error while updating database file: "+self.URL_FILE)
            logging.error(str(sys.exc_info()[0]))

    def update_blacklist_urldb(self, strurl):
        self.blacklist_url_db.append(strurl)
        try:
            with open(self.BLACKLIST_URL_FILE,"a") as f:
                f.write(strurl+"\n")
                logging.debug("Adding URL: "+str(strurl)+" to black list database.")
        except Exception:
            logging.error("Error while updating blacklist database file: "+self.URL_FILE)
            logging.error(str(sys.exc_info()[0]))

    def initialize_urldb(self):
        try:
            with open(self.URL_FILE, "a") as f:
                self.url_db = self.geturls(f.read())
                logging.debug("URL database initialized: "+self.URL_FILE)
        except Exception:
            logging.error("Unable initialize URL database: "+self.URL_FILE)
            logging.error(str(sys.exc_info()[0]))

    def initialize_blacklist_urldb(self):
        try:
            with open(self.BLACKLIST_URL_FILE, "a") as f:
                self.blacklist_url_db = self.geturls(f.read())
                logging.debug("Blacklist URL database initialized: "+self.BLACKLIST_URL_FILE)
        except Exception:
            logging.error("Unable to initialize blacklist URL db: "+self.BLACKLIST_URL_FILE)
            logging.error(str(sys.exc_info()[0]))

    def initialize_logging(self):
        # set up logging to file
        fn = self.LOGGING_FILE
        fm = "a"
        lvl = logging.DEBUG
        fmt = "%(asctime)s - %(levelname)s - %(message)s"
        logging.basicConfig(filename=fn, filemode=fm, level=lvl, format=fmt)
        # set up logging to console
        sh = logging.StreamHandler()
        sh.setLevel(logging.DEBUG)
        sh.setFormatter(logging.Formatter(fmt))
        # add the handler to the root logger
        logging.getLogger('').addHandler(sh)
        logger = logging.getLogger(__name__)
        logger.debug("Logging engine initialized, using file: "+fn)