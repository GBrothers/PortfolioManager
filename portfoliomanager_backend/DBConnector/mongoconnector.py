import json
import pymongo
from Helper import logmngr, configmngr as config, datetimehelper as dth
from Helper import calchelper as calch, internalfilewriter as ifw
from DBConnector import cons

from DBConnector.aggregations import aggregations

log = logmngr.get_logger()

log.info("Connecting MongoDB Atlas and Collections...")
dbclient = pymongo.MongoClient(
    config.get_config(
        "database",
        "mongodb-connectionstring"),
    serverSelectionTimeoutMS=3000)
db = dbclient.get_database(
    config.get_config("database", "mongodb-database"))
eod_collection = db.get_collection(
    config.get_config("database", "mongodb-coll-eodhd_eod"))
intraday_collection = db.get_collection(
    config.get_config("database", "mongodb-coll-eodhd_intraday"))
stock_fundamentals_collection = db.get_collection(
    config.get_config("database", "mongodb-coll-eodhd-stock-fundamentals"))
exchanges_collection = db.get_collection(
    config.get_config("database", "mongodb-coll-eodhd-exchanges"))
log.info("Database Connection established")


def _add_daydiffs(data):

    prev_close = -9999
    for entry in data["data"]:
        day_diff = calch.calc_decimals(
            entry["close"], entry["open"], calch.MINUS)
        day_diff_perc = calch.calc_diff_perc(
            entry["close"], entry["open"])
        if prev_close == -9999:
            prev_close = entry["close"]
        prev_day_diff = calch.calc_decimals(
            entry["close"], prev_close, calch.MINUS)
        prev_day_diff_perc = calch.calc_diff_perc(
            entry["close"], prev_close)
        prev_close = entry["close"]
        entry["returns"] = day_diff
        entry["returns_perc"] = day_diff_perc
        entry["returns_prev_day"] = prev_day_diff
        entry["returns_prev_day_perc"] = prev_day_diff_perc


def is_mongo_alive():
    try:
        dbclient.server_info()
    except:
        log.error("MongoDB not available at %s", config.get_config(
            "database", "mongodb-connectionstring"))
        return False
    return True


def update_eod_data(ticker, data):
    _add_daydiffs(data)
    ticker = str(ticker).lower()
    try:
        eod_collection.insert_one(data)
        log.info("eod data updated for ticker %s", ticker)
    except RuntimeError as r_e:
        log.error(
            "could not add eod data for %s. %s",
            ticker,
            str(r_e))


def update_stock_fundamentals(ticker, data):
    ticker = str(ticker).lower()
    new_data = {
        'ticker': ticker,
        'inserted': dth.now_as_string(),
        'data': data
    }
    tfilter = {'ticker': ticker}
    stock_fundamentals_collection.replace_one(
        tfilter, new_data, upsert=True)
    log.info("stock fundamentals updated for ticker %s", ticker)


def update_exchange_list(data):
    new_data = {
        'name': 'exchangelist',
        'data': data
    }
    exchanges_collection.replace_one(
        {'name': 'exchangelist'}, new_data, upsert=True)


def get_exchange_list():
    result = exchanges_collection.find_one({'name': 'exchangelist'})
    return json.dumps(result["data"])


def get_available_tickers(exchanges="", eqType=cons.EQUITY_COMMON_STOCK):
    if isinstance(exchanges, str):
        exchanges = [exchanges]
    result = []
    for exchange in exchanges:    
      if len(exchange) > 0:
          exchange = "^" + exchange + "$"
      aggjson = aggregations.get_aggr(
          "list_available_tickers", [exchange, eqType])
      db_result = exchanges_collection.aggregate(aggjson)
      for entry in db_result:
          result.append(entry["Ticker"])
    return result


def update_exchange_tickers(exchange, tickers):
    tickers_types = []
    ex_total = 0
    for ticker in tickers:
        ticker['Type'] = ticker['Type'].upper()
        hasType = False
        for ticker_type in tickers_types:
            if ticker_type["Type"] == ticker["Type"]:
                ticker_type["Tickers"].append(ticker)
                hasType = True
                break
        if not hasType:
            tickers_types.append({
                "Exchange": exchange,
                "Type": ticker['Type'],
                "Tickers": [ticker]
            })
    for ticker_type in tickers_types:
        exchanges_collection.replace_one(
            {'Exchange': exchange, 'Type': ticker_type["Type"]}, ticker_type, upsert=True)
        ex_total += len(ticker_type["Tickers"])
        log.info("Update for %s/%s: input size: %s", exchange,
                 ticker_type["Type"], len(ticker_type["Tickers"]))
    log.info("Updated %s Equities for Exchange %s", ex_total, exchange)
    return ex_total


def check_ticker_exists(ticker):
    ticker = str(ticker).lower()
    return eod_collection.count_documents(
        {"ticker": ticker}, limit=1) != 0


def find_eod_last_first_date(ticker, last_first=-1):
    ticker = str(ticker).lower()
    aggjson = aggregations.get_aggr(
        "eod_last_first_date", [ticker, last_first])
    result = eod_collection.aggregate(aggjson)
    try:
        result = next(result)["data"]["date"]
        return result
    except RuntimeError:
        log.warning("no document for ticker %s found", ticker)
        return ""


def get_eod_data(ticker):
    ticker = str(ticker).lower()
    result = eod_collection.find_one({"ticker": ticker})
    if result is None:
        return None
    return json.dumps(result["data"])


def get_fundamentals(ticker):
    ticker = str(ticker).lower()
    result = stock_fundamentals_collection.find_one(
        {"ticker": ticker})
    if result is None:
        return None
    return json.dumps(result["data"])


def get_fundamentals_tickers():
    result = []
    aggjson = aggregations.get_aggr("list_fundamental_tickers")
    db_result = stock_fundamentals_collection.aggregate(aggjson)
    for entry in db_result:
      result.append(entry["ticker"])
    return result

def get_fundamentals_logo_path(ticker):
    ticker = ticker.lower()
    try:
        aggjson = aggregations.get_aggr(
            "fundamentals_logo_path", ticker)
        result = stock_fundamentals_collection.aggregate(aggjson)
        result = next(result)["LogoURL"]
        log.info("found imagepath %s for %s", result, ticker)
        return result
    except StopIteration:
        log.warning("no imagepath found for ticker %s ", ticker)
        return None


def set_fundamental_logo_path(ticker, path="/img/logos/_DEFAULT.png"):
    stock_fundamentals_collection.update_one(
        {"ticker": ticker}, {"$set": {"data.General.LogoURL": path}})


def find_stock(
        phrase="not_filtered",
        incl_ticker=True,
        incl_name=True,
        incl_exchange=False,
        incl_isin=False):
    ticker = phrase if incl_ticker else 'not_defined'
    name = phrase if incl_name else 'not_defined'
    exchange = phrase if incl_exchange else 'not_defined'
    isin = phrase if incl_isin else 'not_defined'
    aggjson = aggregations.get_aggr(
        "search_ticker", [ticker, name, exchange, isin])
    db_result = stock_fundamentals_collection.aggregate(aggjson)
    return json.dumps(list(db_result))


def main():
    # print(get_fundamentals_logo_path("mcd.us"))
    # print(find_eod_last_first_date("ge.us", -1))
    print(find_stock("oe"))


if __name__ == "__main__":
    main()
