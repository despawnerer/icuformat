# coding=utf-8
from __future__ import unicode_literals

from datetime import datetime, date, time
from functools import wraps
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


def cache_by_locale(f):
    cache = {}

    @wraps(f)
    def wrapper(formatter, *args, **kwargs):
        key = (formatter.locale.getName(), args, tuple(kwargs.items()))
        if key not in cache:
            cache[key] = f(formatter, *args, **kwargs)
        return cache[key]

    return wrapper


class Formatter(object):
    def __init__(self, locale_name):
        self.locale = Locale(locale_name)

    # dates

    def short_date(self, d):
        return self.get_date_format(DateFormat.SHORT).format(force_datetime(d))

    def medium_date(self, d):
        return self.get_date_format(DateFormat.MEDIUM).format(force_datetime(d))

    def long_date(self, d):
        return self.get_date_format(DateFormat.LONG).format(force_datetime(d))

    # times

    def short_time(self, t):
        return self.get_time_format(DateFormat.SHORT).format(force_datetime(t))

    def long_time(self, t):
        return self.get_time_format(DateFormat.LONG).format(force_datetime(t))

    # datetimes

    def short_datetime(self, dt):
        return self.get_datetime_format(
            DateFormat.SHORT, DateFormat.SHORT).format(dt)

    def medium_datetime(self, dt):
        return self.get_datetime_format(
            DateFormat.MEDIUM, DateFormat.SHORT).format(dt)

    def long_datetime(self, dt):
        return self.get_datetime_format(
            DateFormat.LONG, DateFormat.LONG).format(dt)

    # date ranges

    def date_range(self, from_date, to_date):
        interval = DateInterval(force_datetime(from_date),
                                force_datetime(to_date))
        return self.get_date_interval_format().format(interval)

    def datetime_range(self, from_dt, to_dt):
        interval = DateInterval(from_dt, to_dt)
        return self.get_datetime_interval_format().format(interval)

    # numbers

    def number(self, number):
        return self.get_number_format().format(number)

    def spell_out(self, number):
        return self.get_number_format(URBNFRuleSetTag.SPELLOUT).format(number)

    def currency(self, number, currency):
        return self.get_currency_format(currency).format(number)

    # formats

    @cache_by_locale
    def get_date_format(self, style):
        return DateFormat.createDateInstance(style, self.locale)

    @cache_by_locale
    def get_time_format(self, style):
        return DateFormat.createDateInstance(style, self.locale)

    @cache_by_locale
    def get_datetime_format(self, date_style, time_style):
        return DateFormat.createDateTimeInstance(
            date_style, time_style, self.locale)

    @cache_by_locale
    def get_date_interval_format(self):
        return DateIntervalFormat.createInstance('yMMMMd', self.locale)

    @cache_by_locale
    def get_datetime_interval_format(self):
        hour_format = detect_hour_format(self.locale)
        return DateIntervalFormat.createInstance(
            'yMMMMd%sm' % hour_format, self.locale)

    @cache_by_locale
    def get_number_format(self, rule_tag=None):
        if rule_tag is None:
            return NumberFormat.createInstance(self.locale)
        else:
            return RuleBasedNumberFormat(rule_tag, self.locale)

    @cache_by_locale
    def get_currency_format(self, currency):
        format_ = NumberFormat.createCurrencyInstance(self.locale)
        format_.setCurrency(currency)
        return format_


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
