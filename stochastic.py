# coding=utf-8

import datetime
from pprint import pprint
from yahoo_finance import Share


def K(data, by=6):
    """
    K = 100[(C – L5close)/(H5 – L5)]
    C = the most recent closing price
    L5 = the low of the five previous trading sessions
    H5 = the highest price traded during the same 5 day period.

    The formula for the more important D line looks like this:

    D = 100 X (H3/L3)

    Another way to do it is over an amount of moving averages,
    which is what I've chosen to employ.
    """
    close = get_prev_close(data)
    # H5 = get_highest_of(data[1:by])
    # L5 = get_lowest_of(data[1:by])
    # L5Close = get_lowest_of(data[1:by], field='Close')
    H5 = get_highest_of(data)
    L5 = get_lowest_of(data)
    L5Close = get_lowest_of(data, field='Close')

    K = 100 * ( (close - L5Close) / (H5 - L5) )
    return K


def date_as_str(date):
    """
    Takes a datetime object and returns a string
    in the format of "2015-08-19"
    """
    return date.strftime("%Y-%m-%d")


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
            lst.append((k, float(v[field])))
    return lst


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

    key = list(latest.keys())

    # not idiomatic but it's simply the head of the nested dict

    return float(data[0][  key[0]  ]['Close'])


def K_map(data, by=5):

    # kept as anon func so IndexError
    # fails silently

    process = lambda x: K(x, by=by)
    klst = []

    local_data = data.copy()

    while len(local_data) > 0:
        klst.append(process(local_data))
        del local_data[0]

    return klst


def D_map(klst, by=3):
    return moving_average(klst, by=by)


def average(lst):
    return sum(lst) / len(lst)


def moving_average(lst, by=3):
    result = []
    for i, n in enumerate(lst):
        try:
            a = [lst[i + j] for j in range(by)]
            result.append(average(a))
        except IndexError:
            result.append(None)
    return result

def get_dates(data):
    dates = []
    for day in data:
        dates += list(day.keys())
    return dates


class Stochastic(object):
    def __init__(self, stockname, days=10, k_by=6, d_by=3):
        self.data = get_stats(stockname, daycount=days)
        self.k_by = k_by
        self.d_by = d_by
        self.klst = K_map(self.data, self.k_by)
        self.dlst = D_map(self.klst, self.d_by)
