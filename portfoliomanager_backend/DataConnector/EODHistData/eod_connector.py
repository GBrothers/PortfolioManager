import sys
from operator import itemgetter
from datetime import date, datetime, timedelta
import requests
from Helper import configmngr as config, datetimehelper as dth
from Helper import logmngr as log, internalfilewriter as ifw
from DataConnector.EODHistData import common

apitoken = config.get_config('eod historicaldata', 'api-token')
baseurl_intraday = config.get_config(
    'eod historicaldata', 'sub-url-intraday', True)
baseurl_eod = config.get_config('eod historicaldata', 'sub-url-eod', True)

log = log.get_logger()


def _prepare_datetimes(start, end, astimestamps=True):
    start = dth.str2dateordatetime(start)

    if isinstance(end, str):
        if end == 'now':
            end = datetime.now()
        elif end.startswith("+"):
            end = start + timedelta(days=int(end.split("+")[1]))
        end = dth.str2dateordatetime(end, True)
    if end.hour == 0:
        end = end.replace(hour=22)
    if(datetime.weekday(start) > 4) and (datetime.weekday(end) > 4):
        log.warning("Weekend %s - %s", str(start), str(end))
    if astimestamps:
        start = dth.get_timestamp(start)
        end = dth.get_timestamp(end)
    return [start, end]


def _get_start_end_date(data):
    if "data" in data:
        data = data["data"]
    start = min(data, key=itemgetter("date"))
    end = max(data, key=itemgetter("date"))
    return [start["date"], end["date"]]

# !! MOVE to intraday_connector.py !!


def get_intraday(ticker, start=(date.today() - timedelta(days=1)), end='+1', interval='5m'):
    start, end = _prepare_datetimes(start, end)
    log.info("request: %s - > %s - %s", ticker, dth.get_datetime_timestamp(
        start), dth.get_datetime_timestamp(end))
    url = baseurl_intraday + ticker + '?' + 'api_token=' + apitoken + '&fmt=json&from=' + \
        str(start) + '&to=' + str(end) + '&interval=' + interval
    log.info(url)
    response = requests.get(url)
    common.check_response_status(response)
    return response.json()


def get_eod(ticker, start=(date.today() - timedelta(days=1)), end="+1", period="d"):
    start, end = _prepare_datetimes(start, end, False)
    log.info("request: %s - > %s - %s", ticker, start, end)
    url = baseurl_eod + ticker + '?' + 'api_token=' + apitoken + '&fmt=json&from=' + \
        str(start) + '&to=' + str(end) + '&period=' + period
    log.info(url)
    response = requests.get(url)
    common.check_response_status(response)
    internal_data = response.json()
    start, end = _get_start_end_date(internal_data)
    internal_data = {"ticker": ticker, "startdate": start, "enddate": end,
                     "inserted": dth.now_as_string(), "data": internal_data}
    return internal_data


def main(argv):
    if len(argv) == 1:
        print("No Arguments provided!")
        return
    ticker = str(argv[1])
    data = get_eod(ticker, "1980-01-01", "now")
    ifw.write("eod_" + ticker, data)


if __name__ == "__main__":
    main(sys.argv)
