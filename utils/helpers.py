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


def get_series_and_labels_as_xy_dict(entries):
    s1 = []
    s2 = []
    s3 = []
    s4 = []
    lables = []
    i = 0
    for i1, i2, i3, i4, dt in entries:
        print i1, i2, i3, i4, dt
        s1.append({'x': i, 'y': i1})
        s2.append({'x': i, 'y': i2})
        s3.append({'x': i, 'y': i3})
        s4.append({'x': i, 'y': i4})
        lables.append(dt)
        i += 1
    means = (('SERIA1', mean(s1)),
             ('SERIA2', mean(s2)),
             ('SERIA3', mean(s3)),
             ('SERIA4', mean(s4)),
             )
    return json.dumps(s1), json.dumps(s2), json.dumps(s3), json.dumps(s4), json.dumps(lables), means


def mean(numbers):
    if numbers:
        val_list = [x['y'] for x in numbers if x['y'] ]
        return round(float(sum(val_list)) / max(len(val_list), 1), 1)
    return 'None'