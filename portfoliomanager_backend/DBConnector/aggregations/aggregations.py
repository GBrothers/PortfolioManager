import json
import DBConnector.aggregations.__init__ as init
from Helper import logmngr

log = logmngr.get_logger()
aggs = init.aggs


def get_aggr(aggr_name, args = []):
    if isinstance(args, str):
        args = [args]
    elif isinstance(args, int):
        args = [str(args)]
    try:
        agg = str(aggs[aggr_name])
    except KeyError as k_e:
        log.critical("no aggregation found for %s", aggr_name)
        raise k_e
    counter = 1
    for arg in args:
        old_str = "<" + str(counter) + ">"
        agg = agg.replace(old_str, str(arg))
        counter += 1
    return json.loads(agg)
