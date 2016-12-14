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
def hello_world():
    db = get_db()
    cur = db.execute('select ia7, ia8, ia14, ia15 from board  where ia14 is not null order by id desc')
    entries = cur.fetchall()
    return render_template('index.html', entries=entries)



@app.route('/db', methods=['GET'])
def bd_save_external_data():
    if request.method == 'GET':
        db = get_db()
        db.execute('insert into board (ia7, ia8, ia14, ia15) values (?, ?, ?, ?)',
                   [request.args.get('ia7'),
                    request.args.get('ia8'),
                    request.args.get('ia14'),
                    request.args.get('ia15')])
        db.commit()
    return 'ok'