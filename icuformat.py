# coding=utf-8
from __future__ import unicode_literals

from datetime import datetime, date, time
from icu import (
    Locale,
    DateInterval,
    DateIntervalFormat,
    DateFormat,
    NumberFormat,
    RuleBasedNumberFormat,
    URBNFRuleSetTag,
)


__all__ = ['Formatter']


class Formatter(object):
    def __init__(self, locale):
        self.locale = Locale(locale)

        self._short_date_format = DateFormat.createDateInstance(
            DateFormat.SHORT, self.locale)
        self._medium_date_format = DateFormat.createDateInstance(
            DateFormat.MEDIUM, self.locale)
        self._long_date_format = DateFormat.createDateInstance(
            DateFormat.LONG, self.locale)

        self._short_time_format = DateFormat.createTimeInstance(
            DateFormat.SHORT, self.locale)
        self._long_time_format = DateFormat.createTimeInstance(
            DateFormat.LONG, self.locale)

        self._short_datetime_format = DateFormat.createDateTimeInstance(
            DateFormat.SHORT, DateFormat.SHORT, self.locale)
        self._medium_datetime_format = DateFormat.createDateTimeInstance(
            DateFormat.MEDIUM, DateFormat.SHORT, self.locale)
        self._long_datetime_format = DateFormat.createDateTimeInstance(
            DateFormat.LONG, DateFormat.LONG, self.locale)

        hour_format = detect_hour_format(self.locale)
        self._date_range_format = DateIntervalFormat.createInstance(
            'yMMMMd', self.locale)
        self._datetime_range_format = DateIntervalFormat.createInstance(
            'yMMMMd%sm' % hour_format, self.locale)

        self._number_format = NumberFormat.createInstance(self.locale)
        self._spell_out_format = RuleBasedNumberFormat(
            URBNFRuleSetTag.SPELLOUT, self.locale)

    # dates

    def short_date(self, d):
        return self._short_date_format.format(force_datetime(d))

    def medium_date(self, d):
        return self._medium_date_format.format(force_datetime(d))

    def long_date(self, d):
        return self._long_date_format.format(force_datetime(d))

    # times

    def short_time(self, t):
        return self._short_time_format.format(force_datetime(t))

    def long_time(self, t):
        return self._long_time_format.format(force_datetime(t))

    # datetimes

    def short_datetime(self, dt):
        return self._short_datetime_format.format(dt)

    def medium_datetime(self, dt):
        return self._medium_datetime_format.format(dt)

    def long_datetime(self, dt):
        return self._long_datetime_format.format(dt)

    # date ranges

    def date_range(self, from_date, to_date):
        interval = DateInterval(force_datetime(from_date),
                                force_datetime(to_date))
        return self._date_range_format.format(interval)

    def datetime_range(self, from_dt, to_dt):
        interval = DateInterval(from_dt, to_dt)
        return self._datetime_range_format.format(interval)

    # numbers

    def number(self, number):
        return self._number_format.format(number)

    def spell_out(self, number):
        return self._spell_out_format.format(number)

    def currency(self, amount, currency):
        formatter = NumberFormat.createCurrencyInstance(
            self.locale)
        formatter.setCurrency(currency)
        return formatter.format(amount)


def force_datetime(value):
    if isinstance(value, date):
        return datetime(value.year, value.month, value.day)
    elif isinstance(value, time):
        now = datetime.now()
        return datetime(now.year, now.month, now.day, value.hour,
                        value.minute, value.second, value.microsecond)
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
