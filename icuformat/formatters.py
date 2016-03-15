from functools32 import lru_cache
from icu import (
    DateIntervalFormat,
    DateFormat,
    SimpleDateFormat,
    NumberFormat,
    RuleBasedNumberFormat,
)


STYLES_FOR_FORMATS = {
    'short': DateFormat.kShort,
    'medium': DateFormat.kMedium,
    'long': DateFormat.kLong,
    'full': DateFormat.kFull,
}


@lru_cache()
def get_date(format_, locale):
    if format_ in STYLES_FOR_FORMATS:
        style = STYLES_FOR_FORMATS[format_]
        return DateFormat.createDateInstance(style, locale)
    else:
        return SimpleDateFormat(format_, locale)


@lru_cache()
def get_time(format_, locale):
    if format_ in STYLES_FOR_FORMATS:
        style = STYLES_FOR_FORMATS[format_]
        return DateFormat.createTimeInstance(style, locale)
    else:
        return SimpleDateFormat(format_, locale)


@lru_cache()
def get_datetime(format_, time_format, locale):
    if format_ in STYLES_FOR_FORMATS and time_format in STYLES_FOR_FORMATS:
        date_style = STYLES_FOR_FORMATS[format_]
        time_style = STYLES_FOR_FORMATS[time_format]
        return DateFormat.createDateTimeInstance(
            date_style, time_style, locale)
    else:
        return SimpleDateFormat(format_, locale)


@lru_cache()
def get_date_interval(locale):
    return DateIntervalFormat.createInstance('yMMMMd', locale)


@lru_cache()
def get_datetime_interval(locale):
    hour_format = _detect_hour_format(locale)
    return DateIntervalFormat.createInstance(
        'yMMMMd%sm' % hour_format, locale)


@lru_cache()
def get_number(locale, rule_tag=None):
    if rule_tag is None:
        return NumberFormat.createInstance(locale)
    else:
        return RuleBasedNumberFormat(rule_tag, locale)


@lru_cache()
def get_percent(locale):
    return NumberFormat.createPercentIntstance(locale)


@lru_cache()
def get_currency(currency, locale):
    format_ = NumberFormat.createCurrencyInstance(locale)
    format_.setCurrency(currency)
    return format_


def _detect_hour_format(locale):
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
