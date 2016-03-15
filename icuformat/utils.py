from datetime import date, datetime, time


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
