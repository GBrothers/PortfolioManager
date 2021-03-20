import os
import pathlib
import json

path = pathlib.Path(__file__).parent.absolute()
aggs = {}

print("Initializing DBConnector Aggregations")
for file in os.listdir(path):
    if file.endswith(".json"):
        name = file.split(".json")[0]
        data = open(path.as_posix() + "/" + file, "r").read()
        # data = json.load(open(path.as_posix() + "/" + file))
        aggs.update({name: data})
        print(file + " added")
print("DBConnector Aggregations with " +
      str(len(aggs)) + " entries initialized")
