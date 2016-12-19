import os
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

from utils.helpers import get_series_and_labels, get_query_with_time_delta, get_series_and_labels_as_xy_dict

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
    return render_template('index.html', limit=DATA_LIMIT)



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


@app.route('/d3nv-24h')
def d3nv_view():
    data_limit = 24
    db = get_db()
    select = get_query_with_time_delta(data_limit)
    cur = db.execute(select)
    entries = cur.fetchall()
    s1, s2, s3, s4, dt, means = get_series_and_labels_as_xy_dict(entries)
    return render_template('d3nv-chart.html', s1=s1, s2=s2, s3=s3, s4=s4, dt=dt, limit=data_limit, means=means)

@app.route('/d3nvalldata')
def d3nv_view_all():
    data_limit = 8760
    db = get_db()
    select = get_query_with_time_delta(data_limit)
    cur = db.execute(select)
    entries = cur.fetchall()
    s1, s2, s3, s4, dt, means = get_series_and_labels_as_xy_dict(entries)
    return render_template('d3nv-chart.html', s1=s1, s2=s2, s3=s3, s4=s4, dt=dt, limit=data_limit, means=means)

@app.route('/d3nv-week')
def d3nv_view_all():
    data_limit = 24 * 7
    db = get_db()
    select = get_query_with_time_delta(data_limit)
    cur = db.execute(select)
    entries = cur.fetchall()
    s1, s2, s3, s4, dt, means = get_series_and_labels_as_xy_dict(entries)
    return render_template('d3nv-chart.html', s1=s1, s2=s2, s3=s3, s4=s4, dt=dt, limit=data_limit, means=means)

