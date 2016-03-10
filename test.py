from datetime import date, datetime, time
from icuformat import Format

en = Format('en_US')
ru = Format('ru')

for formatter in (ru, en):
    print()
    print(formatter.locale.getDisplayName())
    print("-- dates")
    print(formatter.date(date(2016, 3, 5), format='short'))
    print(formatter.date(date(2016, 3, 5), format='medium'))
    print(formatter.date(date(2016, 3, 5), format='long'))
    print("-- times")
    print(formatter.time(time(10, 0), format='short'))
    print(formatter.time(time(15, 0), format='long'))
    print("-- datetimes")
    print(formatter.datetime(datetime(2010, 5, 6, 15, 0), format='short'))
    print(formatter.datetime(datetime(2010, 5, 6, 15, 0), format='medium', time_format='short'))
    print(formatter.datetime(datetime(2010, 5, 6, 15, 0), format='long'))
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
