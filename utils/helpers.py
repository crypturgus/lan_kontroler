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
    d = {}
    data = []
    s1 = []
    s2 = []
    s3 = []
    s4 = []
    lables = []
    for i1, i2, i3, i4, dt in entries:
        print i1, i2, i3, i4, dt
        s1.append({'x': dt, 'y': i1})
        s2.append({'x': dt, 'y': i2})
        s3.append({'x': dt, 'y': i3})
        s4.append({'x': dt, 'y': i3})
    # print s1
    # print s2
    # print s3
    # print s4
    return json.dumps(s1), json.dumps(s2), json.dumps(s3), json.dumps(s4),

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
    # return json.dumps(ia7), json.dumps(ia8), json.dumps(ia14), json.dumps(ia15), json.dumps(dt)
