import datetime
import json

from flask import (
    request,
    render_template,
)
from .models import Board

from utils.helpers import (
    get_corect_datetime_limit,
    get_stats,
    prepare_data,
    set_correct_series_names,
)

from app import app, db


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
        stats_data = get_stats(series_data)
        if not request.args:
            request_data = {"series1": "on", "time_delta": "12", "series2": "on", "series3": "on", "interval_type": "hours", "series4": "on"}
        else:
            request_data = {k: str(v) for k, v in request.args.items()}
            print type(request_data)

        set_correct_series_names(series_data)

        return render_template('chart.html',
                               series_data=json.dumps(series_data),
                               stats_data=stats_data,
                               request_data=request_data,
                               )
    else:
        return 'O szit!'



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

