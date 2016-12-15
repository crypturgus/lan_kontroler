import datetime

import sqlite3

from helpers import get_query_with_time_delta, get_series_and_labels, get_series_and_labels_as_xy_dict

select = get_query_with_time_delta(100)
print select
hour_before = datetime.datetime.now().replace(microsecond=0) -datetime.timedelta(hours=4)
conn = sqlite3.connect('../lancontrol.db')
cur = conn.execute(select)
entries = cur.fetchall()
# print entries

s1, s2, s3, s4, dt = get_series_and_labels(entries)
# print datetime.datetime.now().replace(microsecond=0) -datetime.timedelta(hours=1)
print s1
print s2
print s3
print s4
print dt

get_series_and_labels_as_xy_dict(entries)

# d = {}
# data  = [ ]
#
# for i1, i2, i3, i4, dt in entries:
#     print i1, i2, i3, i4, dt
#     d['ia7'] = i1
#     d['ia8'] = i2
#     d['ia14'] = i3
#     d['ia15'] = i4
#     d['dt'] = dt
#     data.append(d)
#     d = {}
# ia7 = [x['ia7'] for x in data]
# ia8 = [x['ia8'] for x in data]
# ia14 = [x['ia14'] for x in data]
# ia15 = [x['ia15'] for x in data]
# dt = [x['dt'] for x in data]
