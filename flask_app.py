import os
import re

import sqlite3
from flask import (
    Flask,
    request,
    session,
    g,
    redirect,
    url_for,
    abort,
    render_template,
    flash,
)

from utils.helpers import (
    get_series_and_labels,
    get_query_with_time_delta,
    get_series_and_labels_as_xy_dict,
    interval_type_to_hours,
)

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'lancontrol.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='admin'
))
app.config.from_envvar('FLASK_APP_SETTINGS', silent=True)
# boardchart



def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print 'Initialized the database.'


@app.route('/')
def index():
    return redirect(url_for('get_view')+'-1h-1-1-0-0')
    # return render_template('index.html', limit='??')



@app.route('/db', methods=['GET'])
def bd_save_external_data():
    if request.method == 'GET':
        db = get_db()
        ia8 = request.args.get('ia8')
        if ia8 == '-60.0':
            ia8 = None
        db.execute('insert into board (ia7, ia8, ia14, ia15) values (?, ?, ?, ?)',
                   [request.args.get('ia7'),
                    ia8,
                    request.args.get('ia14'),
                    request.args.get('ia15')])
        db.commit()
    return 'ok'


@app.route('/chartist')
def chartist_view():
    data_limit = 24
    db = get_db()
    select = get_query_with_time_delta(data_limit)
    cur = db.execute(select)
    entries = cur.fetchall()
    s1, s2, s3, s4, td = get_series_and_labels(entries)
    return render_template('chartist.html', s1=s1, s2=s2, s3=s3, s4=s4, dt=td, limit=data_limit)


@app.route('/charto')
@app.route('/charto-<int:delta_val><delta_type>')
def chart_base_view(delta_val=24, delta_type='h'):
    if delta_type == 'h':
        data_limit = delta_val
    elif delta_type == 'days':
        data_limit = int(delta_val) * 24
    elif delta_type == 'weeks':
        data_limit = int(delta_val) * 24 * 7
    elif delta_type == 'years':
        data_limit = int(delta_val) * 24 * 7 * 365
    db = get_db()
    select = get_query_with_time_delta(data_limit)
    cur = db.execute(select)
    entries = cur.fetchall()
    s1, s2, s3, s4, dt, means = get_series_and_labels_as_xy_dict(entries)
    return render_template('d3nv-chart.html', s1=s1, s2=s2, s3=s3, s4=s4, dt=dt, limit=data_limit, means=means)


# @app.route('/chart')
@app.route('/charto-<int:delta_val><delta_type>-<int:seria1>-<int:seria2>-<int:seria3>-<int:seria4>')
def chart_base_view_(delta_val=24, delta_type='h', seria1=None, seria2=None, seria3=None, seria4=None):
    if delta_type == 'h':
        data_limit = delta_val
    elif delta_type == 'days':
        data_limit = int(delta_val) * 24
    elif delta_type == 'weeks':
        data_limit = int(delta_val) * 24 * 7
    elif delta_type == 'years':
        data_limit = int(delta_val) * 24 * 7 * 365
    db = get_db()
    select = get_query_with_time_delta(data_limit)
    cur = db.execute(select)
    entries = cur.fetchall()
    s1, s2, s3, s4, dt, means = get_series_and_labels_as_xy_dict(entries)
    if not seria1:
        s1 = []
    if not seria2:
        s2 = []
    if not seria3:
        s3= []
    if not seria4:
        s4 = []
    print dt
    return render_template('d3nv-chart.html', s1=s1, s2=s2, s3=s3, s4=s4, dt=dt, limit=data_limit, means=means)


@app.route('/redir', methods=['POST'])
def redir_view():
    if request.method == 'POST':
        hours = request.form['hours']
        if hours:
            return redirect(url_for('chart_base_view') + '-{}h'.format(hours))
        return redirect(url_for('index'))

# time_delta=12&interval=hours&series1=on&series2=on&series3=on&series4=on
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
        s1, s2, s3, s4, dt, means = get_series_and_labels_as_xy_dict(entries)
        if not request.query_string:
            return render_template("chart.html", s1=s1, s2=s2, s3=s3, s4=s4, dt=dt, limit=time_delta_hours, means=means)
        if not seria1:
            s1 = []
        if not seria2:
            s2 = []
        if not seria3:
            s3 = []
        if not seria4:
            s4 = []
        print dt
        print 'sss'
        print 'sss'
        print s1
        print 'sss'
        print s2
        print 'sss'
        print s3
        print 'sss'
        print s4
        print "dupa"
        print request.query_string
        return render_template("chart.html", s1=s1, s2=s2, s3=s3, s4=s4, dt=dt, limit=time_delta_hours, means=means)

