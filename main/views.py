from flask import render_template, request, redirect, url_for
import datetime

from main import app, db
from main.models import Time_Data, Attraction, Opening_time , Show, Show_data, Daily_close
from main.post import check_park
from main.data import get_data, get_shows


def park_name(park):
    if park == 'tdl':
        return '東京ディズニーランド'
    elif park == 'tds':
        return '東京ディズニーシー'

@app.route("/")
def top():
    return redirect('/tdl/today')

@app.route("/<string:park>/today")
def today(park):
    date_str = datetime.datetime.now().strftime('%Y-%m-%d')
    return redirect(f'/{park}/{date_str}')

@app.route("/<string:park>/yesterday")
def yesterday(park):
    date_time = datetime.datetime.now() - datetime.timedelta(days=1)
    date_str = date_time.strftime('%Y-%m-%d')
    return redirect(f'/{park}/{date_str}')

@app.route('/<string:park>/<string:date_str>')
def daily(park, date_str):
    date_time = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    date = date_time.date()
    park_id = check_park(park=park)
    closes, notag_df, tag_df, p_df = get_data(park_id=park_id, date=date)
    tables = []
    for df in [tag_df, notag_df, p_df]:
        table = df.to_html(classes=['table', 'table-sm', 'table-striped', 'table-bordered', 'border-1', 'text-secondary', 'table-light'])
        table = table.replace('<table', '<table style="text-align: center;"')
        table = table.replace('<tr style="text-align: right;"', '<tr"')
        tables.append(table)
    opening_time = Opening_time.query.filter_by(date=date).filter_by(park=park_id).all()
    shows = get_shows(date=date, park_id=park_id)
    park = park_name(park=park)
    return render_template('daily.html', tables=tables, park=park, date_time=date_time, opening_time=opening_time, shows=shows, closes=closes)

@app.route('/search', methods=['POST'])
def search():
    park = request.form.get('park')
    date = request.form.get('date')
    return redirect(f'/{park}/{date}')


@app.route('/attractions')
def attractions():
    attractions = Attraction.query.all()
    return render_template('attractions.html', attractions=attractions)

@app.route('/attractions/alias/<int:id>', methods=['POST'])
def alias(id):
    name = request.form.get('alias')
    attraction = Attraction.query.get(id)
    if name != '':
        attraction.alias = name
        db.session.commit()
        return redirect('/attractions')
    else:
        attraction.alias = None
        db.session.commit()
        return redirect('/attractions')

@app.route('/wait-time/<string:date_str>')
def wait_time_list(date_str):
    date_time = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    date = date_time.date()
    data_list = Time_Data.query.filter_by(date=date).all()
    return render_template('wait_time.html', data_list=data_list, date_time=date_time)

@app.route('/wait-time/search', methods=['POST'])
def admin_search():
    date = request.form.get('date')
    return redirect(f'/wait-time/{date}')

@app.route("/wait-time/today")
def admin_today():
    date_str = datetime.datetime.now().strftime('%Y-%m-%d')
    return redirect(f'/wait-time/{date_str}')