from datetime import datetime, time, date


def str2dateordatetime(date_as_string, forcedatetime=False, dateformat='%Y-%m-%d'):

    if isinstance(date_as_string, datetime):
        return date_as_string

    if isinstance(date_as_string, date):
        if forcedatetime:
            date_as_string = datetime(
                date_as_string.year, date_as_string.month, date_as_string.day, 0, 0, 0)
        return date_as_string

    try:
        result = datetime.strptime(date_as_string, dateformat).date()
        if forcedatetime:
            return datetime(result.year, result.month, result.day)
        return result

    except RuntimeError:
        return str2datetime(date_as_string)


def str2timeordatetime(time_as_string, dateformat='%H:%M:%S'):
    if isinstance(time_as_string, time) or isinstance(time_as_string, datetime):
        return time_as_string
    return datetime.strptime(time_as_string, dateformat).time()


def str2datetime(datetime_as_string, dateformat='%Y-%m-%d %H:%M:%S'):
    return datetime.strptime(datetime_as_string, dateformat)


def date2str(_date, dateformat='%Y-%m-%d'):
    return date.strftime(_date, dateformat)


def time2str(_time, dateformat='%H:%M:%S'):
    return time.strftime(_time, dateformat)


def datetime2str(_datetime, dateformat='%Y-%m-%d %H:%M:%S'):
    return datetime.strftime(_datetime, dateformat)


def get_timestamp(_date, _time=time(0, 0, 0)):
    if isinstance(_date, str):
        _date = str2dateordatetime(_date)
    if isinstance(_time, str):
        _time = str2timeordatetime(_time)

    if isinstance(_date, datetime):
        return _date.timestamp()
    else:
        return datetime.combine(_date, _time).timestamp()


def get_datetime_timestamp(_timestamp):
    return datetime.fromtimestamp(_timestamp)


def now_as_string():
    return datetime2str(datetime.now())


def main():
    dt0 = date(2021, 2, 16)
    tt0 = time(12, 30, 15)
    dt1 = datetime(2021, 2, 16, 0, 0, 0)
    dt2 = datetime(2021, 2, 16, 12, 30, 15)
    tts = get_timestamp(dt2)

    print(get_timestamp(dt0))
    print(get_timestamp("2021-02-16"))
    print(get_timestamp(dt1))

    print(get_timestamp(dt0, tt0))
    print(get_timestamp(dt2))
    print(get_timestamp("2021-02-16 12:30:15"))
    print(get_timestamp("2021-02-16", "12:30:15"))

    print(date2str(dt0))
    print(time2str(tt0))
    print(datetime2str(dt2))

    print(tts, " -> ", get_datetime_timestamp(tts))
    print("now as string: " + now_as_string())


if __name__ == "__main__":
    main()
