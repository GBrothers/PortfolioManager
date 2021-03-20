import os
import urllib.request
import requests
from Helper import logmngr as log, configmngr as config

_apitoken = config.get_config('eod historicaldata', 'api-token')
_baseurl_fundamental = config.get_config(
    'eod historicaldata', 'sub-url-fundamental', True)
_baseurl_logo = config.get_config('eod historicaldata', 'logo-url')
_logo_file_path = config.get_config('database', 'filesys-logo-path')

log = log.get_logger()


def get_index_constituents(index, incl_delist=False, only_ticker=True):
    log.info("request constituents of %s", index)
    url = _baseurl_fundamental + index + '?' + \
        "api_token=" + _apitoken + "&fmt=json"
    log.info(url)
    result = requests.get(url).json()
    if not incl_delist:
        result = result["Components"]
    else:
        result = result["HistoricalTickerComponents"]
    if only_ticker:
        tickers = []
        for i in result:
            entry = result[i]
            tickers.append(entry["Code"]+"."+entry["Exchange"])
        result = tickers
    log.info("found %s constituents for index %s", len(result), index)
    return result


def download_logo(ticker, sub_url):
    log.info("request logo for %s", ticker)
    url = _baseurl_logo + sub_url
    log.info(url)
    logodir = _logo_file_path + (str(sub_url).rsplit('/', 1)[0])[1:]
    if not os.path.exists(logodir):
        os.makedirs(logodir)
    urllib.request.urlretrieve(url, _logo_file_path + sub_url)
    log.info("logo for %s downloaded to %s", ticker, _logo_file_path + sub_url)


def get_stock_fundamentals(ticker):
    log.info("request fundamentals for %s", ticker)
    url = _baseurl_fundamental + ticker + '?' + \
        "api_token=" + _apitoken + "&fmt=json"
    log.info(url)
    result = requests.get(url).json()
    return result


def main():
    print("No main function implemented")


if __name__ == "__main__":
    main()
