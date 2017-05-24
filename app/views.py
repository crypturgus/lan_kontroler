import datetime
import os
import json

import sqlite3
from flask import (
    Flask,
    request,
    g,
    redirect,
    url_for,
    render_template,
)
from .models import Board, User
from utils.helpers import (
    get_reduce_indexes,
    get_series_and_labels,
    get_query_with_time_delta,
    get_series_and_labels_as_xy_dict,
    interval_type_to_hours,
    get_corect_datetime_limit,
    get_stats,
)
from app import app, db
from sqlalchemy.dialects import sqlite

# # create our little application :)
# app = Flask(__name__)
# app.config.from_object(__name__)
#
# # Load default config and override config from an environment variable
# app.config.update(dict(
#     DATABASE=os.path.join(app.root_path, 'lancontrol.db'),
#     SECRET_KEY='development key',
#     USERNAME='admin',
#     PASSWORD='admin'
# ))
# app.config.from_envvar('FLASK_APP_SETTINGS', silent=True)


# def connect_db():
#     """Connects to the specific database."""
#     rv = sqlite3.connect(app.config['DATABASE'])
#     rv.row_factory = sqlite3.Row
#     return rv
#
#
# def get_db():
#     """Opens a new database connection if there is none yet for the
#     current application context.
#     """
#     if not hasattr(g, 'sqlite_db'):
#         g.sqlite_db = connect_db()
#     return g.sqlite_db
#
#
# @app.teardown_appcontext
# def close_db(error):
#     """Closes the database again at the end of the request."""
#     if hasattr(g, 'sqlite_db'):
#         g.sqlite_db.close()
#
#
# def init_db():
#     db = get_db()
#     with app.open_resource('schema.sql', mode='r') as f:
#         db.cursor().executescript(f.read())
#     db.commit()
#
#
# @app.cli.command('initdb')
# def initdb_command():
#     """Initializes the database."""
#     init_db()
#     print 'Initialized the database.'
#

# @app.route('/t',  methods=['GET'])
# def index2():
#     # time_delta=1&interval_type=hours&series1=on&series2=on
#     data = 'DUPA'
#     if request.method == 'GET':
#         request_correct_dict = {}
#         for key in request.args:
#             if hasattr(Board, key):
#                 vals = request.args.get(key)
#                 request_correct_dict[key] = vals
#         board = Board(**request_correct_dict)
#         db.session.add(board)
#         db.session.commit()
#         print data
#     return render_template('chart0.html', data=data)
SERIES_TO_COLUMNS = {
    'series1': 'ia7',
    'series2': 'ia8',
    'series3': 'ia14',
    'series4': 'ia15',
    'dt': 'dt'
}
COLUMNS_TO_SERIES = {v: k for k, v in SERIES_TO_COLUMNS.iteritems()}

def get_columns_name(request_data):
    col_names = []
    for k, v in request_data.iteritems():
        if k.startswith('series') and v == 'on':
            col_names.append(SERIES_TO_COLUMNS[k])
    return col_names


@app.route('/t',  methods=['GET'])
def chart_simple_use():
    data = []
    # ia7, ia8, ia14, ia15, dt
    if request.method == 'GET':
        if not request.args:
            return render_template('chart0.html', data=data)
        col_names = get_columns_name(request.args)

        time_detla = get_corect_datetime_limit(request.args)
        print time_detla

        columns_list = []
        for col_ in col_names:
            columns_list.append(getattr(Board, col_))
        columns_list.append(Board.dt)

        now_ = datetime.datetime.now()
        time_min = now_ - datetime.timedelta(hours=time_detla)
        series_data = []
        dd = {}
        series_len = len(columns_list)
        col_names.append('dt')
        for c in col_names:
            s = COLUMNS_TO_SERIES[c]
            dd[c] = {'key': s, 'values': [], 'color': ''}
        xlable_data = []
        for i_, row in enumerate(db.session.query(*columns_list).filter(columns_list[-1] >= time_min).order_by(columns_list[-1].desc())):
            series_data.append(row)
            for i, d in enumerate(row):
                if col_names[i] == 'dt':
                    # xlable_data.append(d.strftime("%Y-%m-%d %H:%M:%S"))
                    continue
                # dd[col_names[i]]['values'].appenad({'x': i_, 'y': d})

                # dd[col_names[i]]['values'].append(d)
        data = dd
        dd['xlabel'] = xlable_data
        print data
    return render_template('chart0.html', data=data)


@app.route('/', methods=['GET'])
@app.route('/chart', methods=['GET'])
def index():
    if request.method == 'GET':
        if request.args:
            time_detla = get_corect_datetime_limit(request.args)
        else:
            time_detla = 12
        now_ = datetime.datetime.now().replace(microsecond=0)
        time_min = now_ - datetime.timedelta(hours=time_detla)
        used_series = [s for s, v in request.args.items() if s.startswith('series') and v == 'on']
        data_from_db = Board.query.filter(Board.dt >= time_min).with_entities(Board.ia7, Board.ia8, Board.ia14, Board.ia15, Board.dt).all()
        if used_series:
            series_data = prepare_data(data_from_db, used_series)
        else:
            series_data = prepare_data(data_from_db)
        min_list = []
        max_list = []
        for s in series_data['series']:
            y = [k['y'] for k in s['values']]
            if y:
                min_list.append(min(y))
                max_list.append(max(y))
        stats_data = get_stats(series_data)
        if not request.args:
            request_data = {"series1": "on", "time_delta": "12", "series2": "on", "series3": "on", "interval_type": "hours", "series4": "on"}
        else:
            request_data = {k: str(v) for k, v in request.args.items()}
            print type(request_data)
        return render_template('chart.html',
                               series_data=json.dumps(series_data),
                               stats_data=stats_data,
                               request_data=request_data
                               )
    else:
        return 'O szit!'

def prepare_data(sensor, used_series=('series1','series2','series3', 'series4' )):
    sensor = reduce_data(sensor)
    tickValues = []
    series1 = {"color": "#800000", "values": [], 'key': 'series1'}
    series2 = {"color": "#ff7f0e", "values": [], 'key': 'series2'}
    series3 = {"color": "#000080", "values": [], 'key': 'series3'}
    series4 = {"color": "#000080", "values": [], 'key': 'series4'}
    dt = {"xlabel": []}
    for i, row in enumerate(sensor):
        series1['values'].append({'x': i, 'y': row.ia7})
        series2['values'].append({'x': i, 'y': row.ia8})
        series3['values'].append({'x': i, 'y': row.ia14})
        series4['values'].append({'x': i, 'y': row.ia15})
        # dt['xlabel'].append(row.dt.strftime('%Y-%m-%d %H:%M:%S'))
        dt['xlabel'].append(row.dt.strftime('%d-%m-%Y %H:%M'))

        tickValues.append(i)
    correct_series_data =[s for s in [series1, series2, series3, series4]
                          if s['key'] in used_series]
    series_data = {'series': correct_series_data, 'tickValues': tickValues}
    series_data.update(dt)
    return series_data


def reduce_data(sensor):
    len_entries = len(sensor)
    max_len_data = 60 / 3 * 24
    # max_len_data = 15

    if len_entries >= max_len_data:
        red_indexes = get_reduce_indexes(len_entries, max_len_data)
        new_entries = [sensor[i] for i in red_indexes]
        sensor = new_entries
    return sensor


@app.route('/db2', methods=['GET'])
def bd_save_data():
    if request.method == 'GET':
        nd = {}
        l = []
        r = User()
        for key in request.args:
            if hasattr(User, key):
                vals = request.args.get(key)
                nd[key] = vals
                l.append(getattr(User, key))
        # for k, v in nd.iteritems():
        dupa = nd
        user = User(name='Adam', des='Jones')
        # user = User(**nd)
        # db.session.add(user)
        # db.session.commit()
        # dupa = User.query.filter(*l).limit(12).all()
        # dupa = User.query.filter(User.name, User.des).all()
        dupa = User.query.filter(User.name).all()
        dupa = User.query.filter(User.name == 'Adam').all()
        print dupa
        return render_template('chart.html', dupa=dupa)

@app.route('/db', methods=['GET'])
def save_external_data():
    if request.method == 'GET':
        request_correct_dict = {}
        for key in request.args:
            if hasattr(Board, key):
                val = request.args.get(key)
                request_correct_dict[key] = val
        board = Board(**request_correct_dict)
        db.session.add(board)
        db.session.commit()
    return True

# @app.route('/db', methods=['GET'])
# def bd_save_external_data():
#     if request.method == 'GET':
#         db = get_db()
#         ia8 = request.args.get('ia8')
#         if ia8 == '-60.0':
#             ia8 = None
#         db.execute('insert into board (ia7, ia8, ia14, ia15) values (?, ?, ?, ?)',
#                    [request.args.get('ia7'),
#                     ia8,
#                     request.args.get('ia14'),
#                     request.args.get('ia15')])
#         db.commit()
#     return 'ok'



# @app.route('/redir', methods=['POST'])
# def redir_view():
#     if request.method == 'POST':
#         hours = request.form['hours']
#         if hours:
#             return redirect(url_for('chart_base_view') + '-{}h'.format(hours))
#         return redirect(url_for('index'))

@app.route('/chart', methods=['GET'])
def get_view():
    if request.method == 'GET':
        time_delta = request.args.get('time_delta')
        if not time_delta:
            time_delta = 12
        interval_type = request.args.get('interval_type')
        if not interval_type:
            interval_type = 'hours'
        time_delta_hours = interval_type_to_hours(interval_type, time_delta)
        seria1 = request.args.get('series1')
        seria2 = request.args.get('series2')
        seria3 = request.args.get('series3')
        seria4 = request.args.get('series4')
        db = get_db()
        select = get_query_with_time_delta(time_delta_hours)
        cur = db.execute(select)
        entries = cur.fetchall()
        len_entries = len(entries)
        max_len_data = 60/3 * 24
        if len_entries >= max_len_data:
            red_indexes = get_reduce_indexes(len_entries, max_len_data)
            new_entries = [entries[i] for i in red_indexes]
            entries = new_entries
        s1, s2, s3, s4, dt, means = get_series_and_labels_as_xy_dict(entries)
        if not request.query_string:
            request_series = [1] * 4
            return render_template("chart_old.html",
                   s1=s1, s2=s2, s3=s3, s4=s4, dt=dt, limit=time_delta_hours, means=means, request_series=request_series)
        if not seria1:
            s1 = []
        if not seria2:
            s2 = []
        if not seria3:
            s3 = []
        if not seria4:
            s4 = []
        request_series_raw = [seria1, seria2, seria3, seria4]
        request_series = [1 if s else 0 for s in request_series_raw]
        return render_template("chart_old.html",
               s1=s1, s2=s2, s3=s3, s4=s4, dt=dt, limit=time_delta_hours, means=means, request_series=request_series)
