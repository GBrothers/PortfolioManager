import requests
from Helper import logmngr as log
from DataConnector.EODHistData import common

log = log.get_logger()

def getUserData():
    url = common.baseurl_user + '?' + 'api_token=' + common.apitoken
    log.info(url)
    response = requests.get(url)
    return response.json()
