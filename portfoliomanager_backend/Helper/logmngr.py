import logging
from Helper import configmngr as config

confloglevel = config.get_config("application", "log-level")

cases = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
}

logging.basicConfig(format='%(asctime)s %(levelname)s %(filename)s:%(lineno)s %(funcName)s: %(message)s',
                    datefmt='%y/%m/%d/ %H:%M:%S', filename='portfoliomngr.log',
                    encoding='utf-8', level=cases[confloglevel])

def get_logger():
    return logging.getLogger()
