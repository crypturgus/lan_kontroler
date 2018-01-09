import os

import sqlite3
from flask import (
    Flask,
    request,
    g,
    redirect,
    url_for,
    render_template,
)

from utils.helpers import (
    get_reduce_indexes,
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
    return redirect(url_for('get_view'))
    # return render_template('index.html', limit='??')


@app.route('/db', methods=['GET'])
def bd_save_external_data():
    if request.method == 'GET':
        print request.args
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
            return render_template("chart.html",
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
        return render_template("chart.html",
               s1=s1, s2=s2, s3=s3, s4=s4, dt=dt, limit=time_delta_hours, means=means, request_series=request_series)
