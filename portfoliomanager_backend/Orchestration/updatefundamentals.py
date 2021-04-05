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


def update_logo(tickers):
    if isinstance(tickers, str):
        tickers = [tickers]
    start_len = len(tickers)
    end_len = 0
    for ticker in tickers:
        ticker = ticker.lower()
        try:
            url = mongo.get_fundamentals_logo_path(ticker)
            if url == "":
                continue
            eodhd.download_logo(ticker, url)
        except RuntimeError as r_e:
            log.warning("Could not receive logo for %s %s", ticker, r_e)
            continue
        end_len += 1

    if end_len == start_len:
        log.info("Updated %s logos", end_len)
    else:
        log.warning("Updated %s logos but %s expected!", end_len, start_len)


def update_exchange_list():
    mongo.update_exchange_list(eodhd.get_exchange_list())


def update_exchange_tickers():
    for exchange in [{"Code":"US", "Name": "USA"}]: #json.loads(mongo.get_exchange_list()):
        tickers = eodhd.get_exchange_tickers(exchange['Code'])
        mongo.update_exchange_tickers(exchange['Code'], tickers)
        log.info("Updated %s tickers for exchange %s (%s)",
                 len(tickers), exchange['Code'], exchange['Name'])


def main(argv):
    # if len(argv) <= 1:
    #     print("Two Arguments required!")
    #     return

    # update_fundamentals(fund.get_index_constituents('gspc.indx'))
    # update_logo(fund.get_index_constituents('gspc.indx'))
    # update_exchange_list()
    update_exchange_tickers()


if __name__ == "__main__":
    main(sys.argv)
