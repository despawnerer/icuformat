from datetime import date, datetime, time
from functools import wraps

from icu import DateFormat


def cache_by_locale(f):
    cache = {}

    @wraps(f)
    def wrapper(formatter, *args, **kwargs):
        key = (formatter.locale.getName(), args, tuple(kwargs.items()))
        if key not in cache:
            cache[key] = f(formatter, *args, **kwargs)
        return cache[key]

    return wrapper


def force_datetime(value, tzinfo=None):
    if isinstance(value, date):
        return datetime(value.year, value.month, value.day, tzinfo=tzinfo)
    elif isinstance(value, time):
        now = datetime.now()
        return datetime(now.year, now.month, now.day, value.hour,
                        value.minute, value.second, value.microsecond,
                        tzinfo=tzinfo)
    elif isinstance(value, datetime):
        return value
    else:
        raise TypeError


def detect_hour_format(locale):
    format_ = DateFormat.createTimeInstance(DateFormat.SHORT, locale)
    pattern = format_.toPattern()
    if 'h' in pattern:
        return 'h'
    elif 'H' in pattern:
        return 'H'
    elif 'k' in pattern:
        return 'k'
    elif 'K' in pattern:
        return 'K'
    else:
        return 'H'
