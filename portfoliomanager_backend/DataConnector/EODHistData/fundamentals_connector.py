from logging import error
import os
import urllib.request
import requests
from requests.models import HTTPError
from Helper import logmngr as log, configmngr as config
from DataConnector.EODHistData import common

_logo_file_path = config.get_config('database', 'filesys-logo-path')

log = log.get_logger()


def get_index_constituents(index, incl_delist=False, only_ticker=True):
    log.info("request constituents of %s", index)
    url = common.baseurl_fundamental + index + '?' + \
        "api_token=" + common.apitoken + "&fmt=json"
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


def get_exchange_list():
    log.info("request list of exchanges")
    url = common.baseurl_exchange_list + '?' + \
        "api_token=" + common.apitoken + "&fmt=json"
    log.info(url)
    result = requests.get(url).json()
    log.info("found %s exchanges", len(result))
    return result


def get_exchange_tickers(exchange):
    log.info("request all tickers of exchange %s", exchange)
    url = common.baseurl_exchange_tickers + exchange + '?' + \
        "api_token=" + common.apitoken + "&fmt=json"
    log.info(url)
    result = requests.get(url).json()
    log.info("found %s tickers for exchange %s", len(result), exchange)
    return result


def download_logo(ticker, sub_url, force=False):
    url = common.baseurl_logo + sub_url
    logodir = _logo_file_path + (str(sub_url).rsplit('/', 1)[0])[1:]
    if os.path.isfile(_logo_file_path + sub_url) and not force:
        log.info("logo for %s allready exists on path: %s", ticker, _logo_file_path + sub_url)
    else:
        log.info("request logo for %s, URL: %s and Path: %s",
                 ticker, url, logodir)
        if not os.path.exists(logodir):
            os.makedirs(logodir)
        try:
            urllib.request.urlretrieve(url, _logo_file_path + sub_url)
        except urllib.error.HTTPError as httpError:
            log.error("Could not download Logo for %s %s",
                      ticker, str(httpError))
        filesize = os.path.getsize(_logo_file_path + sub_url)
        if filesize < 62:
          log.error("Filesize of %s is just %s",sub_url,filesize)
          os.remove(_logo_file_path + sub_url)
          raise RuntimeError(sub_url + " is corrupted")
        if force:
            log.info("logo for %s replaced on path %s",
                     ticker, _logo_file_path + sub_url)
        else:
            log.info("logo for %s downloaded to %s",
                     ticker, _logo_file_path + sub_url)


def get_stock_fundamentals(ticker):
    log.info("request fundamentals for %s", ticker)
    url = common.baseurl_fundamental + ticker + '?' + \
        "api_token=" + common.apitoken + "&fmt=json"
    log.info(url)
    result = requests.get(url).json()
    return result


def main():
    print("No main function implemented")


if __name__ == "__main__":
    main()
