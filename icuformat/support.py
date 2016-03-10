from icu import (
    Locale,
    DateInterval,
    DateIntervalFormat,
    DateFormat,
    SimpleDateFormat,
    NumberFormat,
    RuleBasedNumberFormat,
    URBNFRuleSetTag,
)

from .utils import cache_by_locale, force_datetime, detect_hour_format


__all__ = ['Format']


STYLES_FOR_FORMATS = {
    'short': DateFormat.kShort,
    'medium': DateFormat.kMedium,
    'long': DateFormat.kLong,
    'full': DateFormat.kFull,
}


class Format(object):
    def __init__(self, locale_name, tzinfo=None):
        self.locale = Locale(locale_name)
        self.tzinfo = tzinfo

    def currency(self, number, currency):
        return self.get_currency_format(currency).format(number)

    def date(self, date, format='medium'):
        datetime = force_datetime(date, self.tzinfo)
        return self.get_date_format(format).format(datetime)

    def date_range(self, from_date, to_date):
        interval = DateInterval(
            force_datetime(from_date, self.tzinfo),
            force_datetime(to_date, self.tzinfo)
        )
        return self.get_date_interval_format().format(interval)

    def datetime(self, datetime, format='medium', time_format=None):
        time_format = time_format or format
        return self.get_datetime_format(format, time_format).format(datetime)

    def datetime_range(self, from_dt, to_dt):
        interval = DateInterval(from_dt, to_dt)
        return self.get_datetime_interval_format().format(interval)

    def decimal(self, number):
        raise NotImplementedError

    def number(self, number):
        return self.get_number_format().format(number)

    def percent(self, number):
        return self.get_percent_format().format(number)

    def time(self, time, format='medium'):
        datetime = force_datetime(time, self.tzinfo)
        return self.get_time_format(format).format(datetime)

    def timedelta(self, delta, granularity='second', threshold=0.85,
                  format='medium', add_direction=False):
        raise NotImplementedError

    def spell_out(self, number):
        return self.get_number_format(URBNFRuleSetTag.SPELLOUT).format(number)

    # formats

    @cache_by_locale
    def get_date_format(self, format_):
        if format_ in STYLES_FOR_FORMATS:
            style = STYLES_FOR_FORMATS[format_]
            return DateFormat.createDateInstance(style, self.locale)
        else:
            return SimpleDateFormat(format_, self.locale)

    @cache_by_locale
    def get_time_format(self, format_):
        if format_ in STYLES_FOR_FORMATS:
            style = STYLES_FOR_FORMATS[format_]
            return DateFormat.createTimeInstance(style, self.locale)
        else:
            return SimpleDateFormat(format_, self.locale)

    @cache_by_locale
    def get_datetime_format(self, format_, time_format):
        if format_ in STYLES_FOR_FORMATS and time_format in STYLES_FOR_FORMATS:
            date_style = STYLES_FOR_FORMATS[format_]
            time_style = STYLES_FOR_FORMATS[time_format]
            return DateFormat.createDateTimeInstance(
                date_style, time_style, self.locale)
        else:
            return SimpleDateFormat(format_, self.locale)

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
    def get_percent_format(self):
        return NumberFormat.createPercentIntstance(self.locale)

    @cache_by_locale
    def get_currency_format(self, currency):
        format_ = NumberFormat.createCurrencyInstance(self.locale)
        format_.setCurrency(currency)
        return format_
