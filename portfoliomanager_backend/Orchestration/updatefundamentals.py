from API.api import get_available_tickers
import sys
import json
import DataConnector.EODHistData.fundamentals_connector as eodhd
import DBConnector.mongoconnector as mongo
from Helper import logmngr

log = logmngr.get_logger()


def update_fundamentals(tickers):
    if isinstance(tickers, str):
        tickers = [tickers]
    start_len = len(tickers)
    end_len = 0
    for ticker in tickers:
        try:
            data = eodhd.get_stock_fundamentals(ticker)
        except RuntimeError as r_e:
            log.error("Could not receive data for %s %s", ticker, r_e)
            continue
        try:
            mongo.update_stock_fundamentals(ticker, data)
        except RuntimeError as r_e:
            log.error("Could not add data for %s to database %s", ticker, r_e)
            continue
        end_len += 1

    if end_len == start_len:
        log.info("Updated %s entries in stock fundamentals", end_len)
    else:
        log.error(
            "Updated %s entries in stock fundamentals but %s expected!", end_len, start_len)


def update_logo(tickers, force = False):
    if isinstance(tickers, str):
        tickers = [tickers]
    start_len = len(tickers)
    end_len = 0
    for ticker in tickers:
        ticker = ticker.lower()
        try:
            url = mongo.get_fundamentals_logo_path(ticker)
            if url == None:
              log.error("Ticker %s not found in database!", ticker)
              continue
            if url == "":
                mongo.set_fundamental_logo_path(ticker)
                log.info("No logo available for %s. Set to default.", ticker)
                continue
            eodhd.download_logo(ticker, url, force)
        except RuntimeError as r_e:
            log.warning("Could not receive logo for %s %s. Set to default!", ticker, r_e)
            mongo.set_fundamental_logo_path(ticker)
            continue
        end_len += 1

    if end_len == start_len:
        log.info("Updated %s logos", end_len)
    else:
        log.warning("Updated %s logos but %s expected!", end_len, start_len)


def update_exchange_list():
    mongo.update_exchange_list(eodhd.get_exchange_list())


def update_exchange_tickers():
    total = 0
    for exchange in json.loads(mongo.get_exchange_list()):
        tickers = eodhd.get_exchange_tickers(exchange['Code'])
        ex_total = mongo.update_exchange_tickers(exchange['Code'], tickers)
        log.info("Updated %s tickers for exchange %s (%s)",
                 len(tickers), exchange['Code'], exchange['Name'])
        total += ex_total
    log.info("Updated a total of %s Equities", total)


def main():
    # update_exchange_list()
    # update_exchange_tickers()
    update_fundamentals(mongo.get_available_tickers())
    update_logo(mongo.get_fundamentals_tickers())
    

if __name__ == "__main__":
    main()
