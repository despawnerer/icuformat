icuformat
=========

`icuformat` is a fast localized date and number formatting library based on ICU.

The API seeks to be a drop-in replacement for Babel with useful additions, but is largely incomplete right now.

It seems, on average, to be 1.5x faster than Babel at formatting dates and times, and more than 10x faster with numbers and currencies.


Example
-------

```python
from datetime import date, datetime, time
from icuformat import Format

formatter = Format('en')
print(formatter.date(date(2015, 9, 12), format='short'))
print(formatter.datetime(datetime(2015, 9, 12, 10, 0)))
print(formatter.time(time(10, 0), format='short'))
```
