from icu import (
    Locale,
    DateInterval,
    URBNFRuleSetTag,
)

from . import formatters
from .utils import force_datetime


__all__ = ['Format']


class Format(object):
    def __init__(self, locale_name, tzinfo=None):
        self.locale = Locale(locale_name)
        self.tzinfo = tzinfo

    def currency(self, number, currency):
        return formatters.get_currency(currency, self.locale).format(number)

    def date(self, date, format='medium'):
        datetime = force_datetime(date, self.tzinfo)
        return formatters.get_date(format, self.locale).format(datetime)

    def date_range(self, from_date, to_date):
        interval = DateInterval(
            force_datetime(from_date, self.tzinfo),
            force_datetime(to_date, self.tzinfo)
        )
        return formatters.get_date_interval(self.locale).format(interval)

    def datetime(self, datetime, format='medium', time_format=None):
        time_format = time_format or format
        return formatters.get_datetime(
            format, time_format, self.locale).format(datetime)

    def datetime_range(self, from_dt, to_dt):
        interval = DateInterval(from_dt, to_dt)
        return formatters.get_datetime_interval(self.locale).format(interval)

    def decimal(self, number):
        raise NotImplementedError

    def number(self, number):
        return formatters.get_number(self.locale).format(number)

    def percent(self, number):
        return formatters.get_percent(self.locale).format(number)

    def time(self, time, format='medium'):
        datetime = force_datetime(time, self.tzinfo)
        return formatters.get_time(format, self.locale).format(datetime)

    def timedelta(self, delta, granularity='second', threshold=0.85,
                  format='medium', add_direction=False):
        raise NotImplementedError

    def spell_out(self, number):
        return formatters.get_number(
            self.locale, URBNFRuleSetTag.SPELLOUT).format(number)
