# Area to play around and test.

import pymongo
from bson.objectid import ObjectId

        
def calculate(number1, number2, operator='+'):
    cases = {
        "+": lambda a, b: a+b,
        "-": lambda a, b: a-b,
        "*": lambda a, b: a*b,
        "/": lambda a, b: a/b,
    }
    return cases[operator](number1, number2)


def main():
    print(calculate(94, 64, "-"))


client = pymongo.MongoClient(
    'mongodb://myUserAdmin:Mongo123@localhost:27017/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false')
col = client['portfoliomngr']['eodhd_stock_fundamentals']


def mongo():
    for doc in col.find():
        pk = ObjectId(str(doc.get("_id")))
        ticker = doc.get('ticker')
        ticker_l = str(ticker).lower()
        print("updating " + ticker + " to " + ticker_l)
        col.update(
            {"_id": pk},
            {'$set': {'ticker': ticker_l}}
        )


if __name__ == "__main__":
    mongo()
