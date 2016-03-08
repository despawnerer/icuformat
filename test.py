from datetime import date, datetime, time
from icuformat import Formatter

en = Formatter('en_US')
ru = Formatter('ru')

for formatter in (ru, en):
    print()
    print(formatter.locale.getDisplayName())
    print("-- dates")
    print(formatter.long_date(date(2016, 3, 5)))
    print(formatter.medium_date(date(2016, 3, 5)))
    print(formatter.short_date(date(2016, 3, 5)))
    print("-- times")
    print(formatter.short_time(time(10, 0)))
    print(formatter.long_time(time(15, 0)))
    print("-- datetimes")
    print(formatter.short_datetime(datetime(2010, 5, 6, 15, 0)))
    print(formatter.medium_datetime(datetime(2010, 5, 6, 15, 0)))
    print(formatter.long_datetime(datetime(2010, 5, 6, 15, 0)))
    print("-- ranges")
    print(formatter.date_range(date(2015, 5, 6), date(2015, 7, 5)))
    print(formatter.datetime_range(
        datetime(2015, 5, 6, 9), datetime(2015, 5, 6, 13)))
    print(formatter.datetime_range(
        datetime(2015, 5, 6, 13), datetime(2015, 5, 6, 14)))
    print("-- numbers")
    print(formatter.number(1000000))
    print(formatter.number(4.56))
    print(formatter.spell_out(5342))
    print(formatter.currency(1234.5, 'USD'))
    print(formatter.currency(1234.5, 'EUR'))
    print(formatter.currency(1234.5, 'RUB'))
