import datetime
import json
import sqlite3

from helpers import get_query_with_time_delta, get_series_and_labels, get_series_and_labels_as_xy_dict, get_correct_dt

select = get_query_with_time_delta(12)
# print select
hour_before = datetime.datetime.now().replace(microsecond=0) -datetime.timedelta(hours=4)
conn = sqlite3.connect('../lancontrol.db')
cur = conn.execute(select)
entries = cur.fetchall()
# print entries

s1, s2, s3, s4, dt = get_series_and_labels(entries)
# print datetime.datetime.now().replace(microsecond=0) -datetime.timedelta(hours=1)
# print s1
# print s2
# print s3
# print s4
# print dt

get_series_and_labels_as_xy_dict(entries)
s1, s2, s3, s4, dt, _ = get_series_and_labels_as_xy_dict(entries)
# print s1
# print s2
# print s3
# print s4
# print dt

td_str = json.loads(dt)
s1 = json.loads(s1)

def get_temp_factor(datetime_labels_str, series):
    datetime_labels = [datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S') for x in datetime_labels_str]
    data = zip(datetime_labels, series)
    start_interval = data[0][0]
    stop_interval = start_interval + datetime.timedelta(hours=1)
    interval_list = []
    all_intervals_list = []
    for d, v in data:
        if d >=start_interval and d<stop_interval:
            interval_list.append((d, v))
        else:
            all_intervals_list.append(interval_list[:])
            interval_list = []
            interval_list.append((d, v))
            start_interval = stop_interval
            stop_interval = start_interval + datetime.timedelta(hours=1)
    result_list = []
    for interval_ in all_intervals_list:
        temperature_list = [single_data[1]['y'] for single_data in interval_]
        print {len(interval_)/2}
        result_list.append(round(temperature_list[-1] - temperature_list[0], 2))
    return result_list
print get_temp_factor(td_str, s1)

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


l = [1, 2, 0, 1, 12, 99, 0]

print [True if s else False for s in l]