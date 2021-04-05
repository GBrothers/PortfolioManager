from Helper import logmngr, configmngr as config

log = logmngr.get_logger()

apitoken = config.get_config('eod historicaldata', 'api-token')
baseurl_intraday = config.get_config(
    'eod historicaldata', 'sub-url-intraday', True)
baseurl_eod = config.get_config('eod historicaldata', 'sub-url-eod', True)
baseurl_fundamental = config.get_config(
    'eod historicaldata', 'sub-url-fundamental', True)
baseurl_user = config.get_config('eod historicaldata', 'sub-url-user', True)
baseurl_logo = config.get_config('eod historicaldata', 'logo-url')
baseurl_exchange_list = config.get_config('eod historicaldata', 'sub-url-exchangelist', True)
baseurl_exchange_tickers = config.get_config('eod historicaldata','sub-url-exchangesymbols', True)

def check_response_status(response):
    if response.status_code != 200:
        log.error("API Server: %s %s", str(
            response.status_code), response.text)
        raise RuntimeError('API Server error: ' +
                           str(response.status_code) + ": " + str(response.text))
