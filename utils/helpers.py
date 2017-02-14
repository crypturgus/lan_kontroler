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
        s1.append({'x': i, 'y': i1})
        s2.append({'x': i, 'y': i2})
        s3.append({'x': i, 'y': i3})
        s4.append({'x': i, 'y': i4})
        lables.append(dt)
        i += 1
    averages = (('SERIA1', series_average(s1)),
                ('SERIA2', series_average(s2)),
                ('SERIA3', series_average(s3)),
                ('SERIA4', series_average(s4)),
                )
    lables = get_correct_dt(lables)
    return json.dumps(s1), json.dumps(s2), json.dumps(s3), json.dumps(s4), json.dumps(lables), averages


def series_average(numbers):
    if numbers:
        val_list = [x['y'] for x in numbers if x['y']]
        return round(float(sum(val_list)) / max(len(val_list), 1), 1)
    return 'None'


def get_stats(series):
    cleared_series = clear_series(series)
    s_max = max(cleared_series)
    s_min = min(cleared_series)
    max_min_diff = s_max - s_min
    stop_start_diff = cleared_series[-1] - cleared_series[0]
    stats_dict = dict(
        min=s_min,
        max=s_max,
        max_min_diff=max_min_diff,
        stop_start_diff=stop_start_diff
    )
    return stats_dict


def clear_series(series):
    '''
    :param series:
    :return: series without None values
    '''
    return [x for x in series if x is not None]


def get_correct_dt(dt):
    return [(datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(hours=1))\
             .strftime("%Y-%m-%d %H:%M:%S")\
            for x in dt]


def interval_type_to_hours(interval_type, interval_val):
    finall_val = int(interval_val)
    if interval_type == 'hours':
        return finall_val
    elif interval_type == 'days':
        return finall_val * 24
    elif interval_type == 'weeks':
        return finall_val * 24 * 7
    elif interval_type == 'all':
        return finall_val * 24 * 12000

def prepare_request(request):
    out0 = request.args.get('out0')
    out1 = request.args.get('out1')
    out2 = request.args.get('out2')
    out3 = request.args.get('out3')
    out4 = request.args.get('out4')
    out5 = request.args.get('out5')
    out6 = request.args.get('out6')
    di0 = request.args.get('di0')
    di1 = request.args.get('di1')
    di2 = request.args.get('di2')
    di3 = request.args.get('di3')
    ia0 = request.args.get('ia0')
    ia1 = request.args.get('ia1')
    ia2 = request.args.get('ia2')
    ia3 = request.args.get('ia3')
    ia4 = request.args.get('ia4')
    ia5 = request.args.get('ia5')
    ia6 = request.args.get('ia6')
    ia7 = request.args.get('ia7')
    ia8 = request.args.get('ia8')
    ia9 = request.args.get('ia9')
    ia10 = request.args.get('ia10')
    ia11 = request.args.get('ia11')
    ia12 = request.args.get('ia12')
    ia13 = request.args.get('ia13')
    ia14 = request.args.get('ia14')
    ia15 = request.args.get('ia15')
    ia166 = request.args.get('ia166')
    ia17 = request.args.get('ia17')
    ia18 = request.args.get('ia18')
    ia19 = request.args.get('ia19')
    freq = request.args.get('freq')
    duty = request.args.get('duty')
    pwm = request.args.get('pwm')
    sec0 = request.args.get('sec0')
    sec1 = request.args.get('sec1')
    sec2 = request.args.get('sec2')
    sec3 = request.args.get('sec3')
    sec4 = request.args.get('sec4')
    request_args = [out0, out1, out2, out3, out4, out5, out6, di0, di1, di2, di3, ia0, ia1, ia2, ia3, ia4, ia5, ia6,
                    ia7, ia8, ia9, ia10, ia11, ia12, ia13, ia14, ia15, ia166, ia17, ia18, ia19, freq, duty, pwm, sec0,
                    sec1, sec2, sec3, sec4]
    normalized_data = [d if d != '-60.0' else None for d in request_args]
    return normalized_data

def get_reduce_indexes(data, max_len=480):

    len_data = len(data)
    factor = len_data / int(max_len)
    print factor
    red_list = [x for x in range(len_data) if x % factor == 0]
    if red_list[-1] != len_data - 1:
        red_list.append(len_data -1)
        print data[len_data - 1]
    return red_list
    