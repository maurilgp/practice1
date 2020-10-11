import logging

class LoggingExample():

    def __init__(self):
        self.initialize_logging()
        logging.debug("---------------Start Program-----------------")
        logging.debug("Hola")
        logging.debug("----------------End Program------------------")

    def initialize_logging(self):
        # set up logging to file
        fn = ".\\tempfiles\LOGGINGEXAMPLE.LOG"
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
