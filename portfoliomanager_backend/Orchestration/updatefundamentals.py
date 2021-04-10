import DataConnector.EODHistData.fundamentals_connector as eodhd
import DBConnector.mongoconnector as mongo
from Helper import logmngr, internalfilewriter as ifw

log = logmngr.get_logger()

US_EXCHANGE_DETAIL = False  # Global Data for all US Exchanges


def update_fundamentals(tickers):
    if isinstance(tickers, str):
        tickers = [tickers]
    start_len = len(tickers)
    end_len = 0
    for ticker in tickers:
        # Workaround, check also last import date!!!!
        if mongo.check_fundamentals_ticker_exists(ticker):
            log.info("ticker %s allready imported", ticker)
            end_len += 1
            continue
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


def update_logo(tickers, force=False):
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
            log.warning(
                "Could not receive logo for %s %s. Set to default!", ticker, r_e)
            mongo.set_fundamental_logo_path(ticker)
            continue
        end_len += 1

    if end_len == start_len:
        log.info("Updated %s logos", end_len)
    else:
        log.warning("Updated %s logos but %s expected!", end_len, start_len)


### ### Exchange Data ### ###
def update_exchange_data():
    final_exchange_tickertypes = []
    exchangelist = eodhd.get_exchange_list()
    for exchange in exchangelist:
        tickers = eodhd.get_exchange_tickers(exchange['Code'])
        if(exchange['Code'] == "US"):
            for us_exchange_tickers in _unwind_us_exchanges(tickers):
                final_exchange_tickertypes.extend(_build_exchange_data(
                    us_exchange_tickers["Exchange"], us_exchange_tickers["Tickers"], True))
        else:
            final_exchange_tickertypes.extend(
                _build_exchange_data(exchange['Code'], tickers, False))
    mongo.update_exchange_tickers(final_exchange_tickertypes)
    mongo.update_exchange_list(_build_exchange_list(
        exchangelist, final_exchange_tickertypes))


def _build_exchange_list(exchangelist, exchange_tickertypes):
    new_exchangelist = []
    global US_EXCHANGE_DETAIL
    for exchange in exchangelist:
        if exchange["Code"] == "US":
            us_exchanges = {}
            for exchange_tickertype in exchange_tickertypes:
                if exchange_tickertype["USExchange"]:
                    if not exchange_tickertype["Exchange"] in us_exchanges:
                        us_exchanges.update(
                            {exchange_tickertype["Exchange"]: []})
                    us_exchanges[exchange_tickertype["Exchange"]].append(
                        exchange_tickertype["Type"])

            for us_exchange in us_exchanges:
                new_us_exchange = {
                    "Name": us_exchange,
                    "Code": us_exchange,
                    "Country": exchange["Country"],
                    "USExchange": True,
                    "Currency": exchange["Currency"],
                    "OperatingMIC": us_exchange,
                    "Types": us_exchanges[us_exchange]
                }
                new_exchangelist.append(
                    _update_exchange_details(new_us_exchange))
        else:
            new_exchange = {
                "Name": exchange["Name"],
                "Code": exchange["Code"],
                "Country": exchange["Country"],
                "USExchange": False,
                "Currency": exchange["Currency"],
                "OperatingMIC": exchange["OperatingMIC"],
                "Types": []
            }
            for exchange_tickertype in exchange_tickertypes:
                if exchange_tickertype["Exchange"] == exchange["Code"]:
                    new_exchange["Types"].append(exchange_tickertype["Type"])
            new_exchangelist.append(_update_exchange_details(new_exchange))
    US_EXCHANGE_DETAIL = False
    return new_exchangelist


def _update_exchange_details(new_exchange):
    global US_EXCHANGE_DETAIL
    if new_exchange["USExchange"] and not US_EXCHANGE_DETAIL:
        US_EXCHANGE_DETAIL = eodhd.get_exchange_details("US")

    details = eodhd.get_exchange_details(
        new_exchange["Code"]) if not new_exchange["USExchange"] else US_EXCHANGE_DETAIL

    new_exchange["Timezone"] = details["Timezone"]
    new_exchange["ExchangeHolidays"] = details["ExchangeHolidays"]
    new_exchange["TradingHours"] = details["TradingHours"]
    new_exchange["ActiveTickers"] = details["ActiveTickers"]
    new_exchange["PreviousDayUpdatedTickers"] = details["PreviousDayUpdatedTickers"]
    return new_exchange


def _build_exchange_data(exchange, tickers, us_exchange):
    UNDEFINED_TYPE = "UNDEFINED"
    exchange_tickertypes = []
    for ticker in tickers:
        if not ticker["Type"]:
            ticker["Type"] = UNDEFINED_TYPE
        ticker['Type'] = ticker['Type'].upper()
        hasType = False
        for exchange_ticker_type in exchange_tickertypes:
            if exchange_ticker_type["Type"] == ticker["Type"]:
                exchange_ticker_type["Tickers"].append(ticker)
                exchange_ticker_type["Size"] += 1
                hasType = True
                break
        if not hasType:
            exchange_tickertypes.append({
                "Exchange": exchange,
                "Type": ticker['Type'],
                "USExchange": us_exchange,
                "Size": 1,
                "Tickers": [ticker]
            })
    return exchange_tickertypes


def _unwind_us_exchanges(tickers):
    UNDEFINED_EXCHANGE = "UNDEFINED"
    us_exchanges_tickers = []
    for ticker in tickers:
        hasType = False
        for us_exchange_tickers in us_exchanges_tickers:
            if not ticker["Exchange"]:
                ticker["Exchange"] = UNDEFINED_EXCHANGE
            if us_exchange_tickers["Exchange"] == ticker["Exchange"]:
                us_exchange_tickers["Tickers"].append(ticker)
                hasType = True
                break
        if not hasType:
            if not ticker["Exchange"]:
                ticker["Exchange"] = UNDEFINED_EXCHANGE
            us_exchanges_tickers.append({
                "Exchange": ticker["Exchange"],
                "Tickers": [ticker]
            })
    return us_exchanges_tickers


def main():
    # update_exchange_data()
    update_fundamentals(mongo.get_available_tickers("NYSE"))
    # update_logo(mongo.get_fundamentals_tickers())


if __name__ == "__main__":
    main()
