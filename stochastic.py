# coding=utf-8

import datetime
from pprint import pprint
from yahoo_finance import Share

def date_as_str(date):
    """
    Takes a datetime object and returns a string
    in the format of "2015-08-19"
    """
    return date.strftime("%Y-%m-%d")


def K(share):
    """
    K = 100[(C – L5close)/(H5 – L5)]
    C = the most recent closing price
    L5 = the low of the five previous trading sessions
    H5 = the highest price traded during the same 5 day period.

    The formula for the more important D line looks like this:

    D = 100 X (H3/L3)

    THINK of this as proportion, and not much more than tat.
    """

    today = datetime.datetime.today()
    todaystr = today.strftime("%Y-%m-%d")
    return 100 * (  )


def get_stats(name, daycount=10):
    """

    :param name: the standard name of the stock
    :param daycount: number of days prior
    :return:
    """

    share = Share(name)
    today = datetime.datetime.today()
    date = today
    daterange = []
    while daycount > 0:
        daterange.append(date_as_str(date))
        date -= datetime.timedelta(days=1)
        daycount -= 1
    data = share.get_historical(daterange[-1], daterange[0])
    return [{date: info} for date in daterange for info in data if date == info['Date']]


def get_last(data, n, field='Close'):
    """
    :param data: list of dicts returned from get_stats
    :param n: number of days to take
    :param field: the field. can be Close, Adj_Close, Symbol, etc.
    :return:
    """
    lst = []
    for day in data[:n]:
        for k, v in day.items():
            yield(k, v[field])


def get_highest_of(data, field='High'):
    high = 0
    # expecting a list of dicts
    for day in data:
        for k, v in day.items():
            if high < float(v[field]):
                high = float(v[field])
    return high


def get_lowest_of(data, field='Low'):
    # make it a million, just to be safe?
    low = 1000000
    # expecting a list of dicts
    for day in data:
        for k, v in day.items():
            if float(v[field]) < low:
                low = float(v[field])
    return low


def get_prev_close(data):
    """without making an api call... """
    # expecting a list of dicts

    latest = data[0].copy()

    # grab the key - there should only be one,
    # but python insists on having the dict_keys type
    # not subscriptable; not treated the same as a list or tuple.

    key = [k for k in latest.keys()]

    # not idiomatic but it's simply the head of the nested dict

    return float(data[0][  key[0]  ]['Close'])


def get_last_five(data):
    pass



print("#"*50)
pprint(get_stats("YHOO"))
print("#"*50)



