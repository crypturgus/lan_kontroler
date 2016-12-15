import datetime
import json


def get_query_with_time_delta(delta=3):
    hour_before = datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(hours=delta)
    return 'select ia7, ia8, ia14, ia15, dt from board  where ia14 is not null and dt > "{}" order by dt ASC'.format(
            hour_before)


def get_series_and_labels(entries):
    d = {}
    data = []
    for i1, i2, i3, i4, dt in entries:
        d['ia7'] = i1
        d['ia8'] = i2
        d['ia14'] = i3
        d['ia15'] = i4
        d['dt'] = dt
        data.append(d)
        d = {}
    ia7 = [x['ia7'] for x in data]
    ia8 = [x['ia8'] for x in data]
    ia14 = [x['ia14'] for x in data]
    ia15 = [x['ia15'] for x in data]
    dt = [x['dt'] for x in data]
    return json.dumps(ia7), json.dumps(ia8), json.dumps(ia14), json.dumps(ia15), json.dumps(dt)

