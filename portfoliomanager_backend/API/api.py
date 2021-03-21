
from flask import Flask, request
from flask_cors import CORS

from Helper import logmngr
from DBConnector import mongoconnector as mc
from DataConnector.EODHistData import user_connector as uc

log = logmngr.get_logger()
app = Flask(__name__)
CORS(app)


@app.errorhandler(404)
def page_not_found():
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/')
def base():
    return "<h1>200</h1><p>Status: Server is UP & RUNNING.</p>"


@app.route('/intern/checkdb', methods=['GET'])
def is_mongodb_alive():
    if mc.is_mongo_alive():
        return 'ok'
    return 'nok'


@app.route('/userdata', methods=['GET'])
def get_user_info():
    response = uc.getUserData()
    if request.args.get('requests'):
        response = {
            'dayrequests': response['apiRequests'],
            'daylimit': response['dailyRateLimit']
        }
    return response


@ app.route('/eod', methods=['GET'])
def get_eod():
    ticker = request.args.get('ticker')
    log.info("Request for %s", ticker)
    result = mc.get_eod_data(ticker)
    return result


@ app.route('/fundamentals', methods=['GET'])
def get_fundamentals():
    if 'ticker' not in request.args:
        return "Error: param ticker not found"
    ticker = request.args.get('ticker')
    log.info("Request for %s", ticker)
    result = mc.get_fundamentals(ticker)
    if result is None:
        log.warning("No Data found for ticker %s", ticker)
        result = "No Data found for ticker " + ticker
    return result


@ app.route('/search', methods=['GET'])
def find_stock():
    if 'phrase' not in request.args and 'fields' not in request.args:
        log.error(
            "neither parameter phrase nor parameter fields provided")
        return "Error: neither parameter phrase nor parameter fields provided"
    phrase = request.args['phrase']
    if 'fields' not in request.args:
        log.info(
            "Request for phrase: %s for default field ticker and name",
            phrase)
        return mc.find_stock(phrase, True, True, False, False)

    field_ticker = "t" in request.args['fields']
    field_name = "n" in request.args['fields']
    field_exchange = "e" in request.args['fields']
    field_isin = "i" in request.args['fields']

    if not field_ticker and not field_name and not field_exchange and not field_isin:
        log.error("no valid field information provided: %s",
                  request.args['fields'])
        return "Error: no valid field information provided! Should be any combination of t, n, e, i"

    log.info("Request for phrase: %s for field: %s",
             phrase, request.args['fields'])
    return mc.find_stock(
        phrase,
        field_ticker,
        field_name,
        field_exchange,
        field_isin)


if __name__ == '__main__':
    if mc.is_mongo_alive():
        app.run(debug=True, port=5001, host='0.0.0.0')
    else:
        print("---------------------------\nError: MongoDB not running!\n---------------------------")
