from main import db
from main.models import Time_Data, Attraction, Opening_time, Show, Show_data, Daily_close
from main.scraping import get_wait_time, get_opening_time, get_show_list, get_close_list_day

import datetime
import schedule


def check_park(park):
    if park == 'tdl':
        park_id = 0
    elif park == 'tds':
        park_id = 1
    return park_id


def post_opening_time(park):
    date = datetime.datetime.now().date()
    park_id = check_park(park=park)
    date_list = Opening_time.query.filter_by(date=date).filter_by(park=park_id).all()
    if len(date_list) != 0:
        date_data = date_list[0]
        open_time = date_data.open_time
        close_time = date_data.close_time
        opening_time = [open_time, close_time]
        return opening_time
    
    else:
        opening_time = get_opening_time(park=park)
        open_time, close_time = opening_time.replace(' ','').split('-')
        open_time = datetime.datetime.strptime(open_time, '%H:%M').time()
        close_time = datetime.datetime.strptime(close_time, '%H:%M').time()
        new_data = Opening_time(date=date, open_time=open_time, close_time=close_time, park=park_id)
        db.session.add(new_data)
        db.session.commit()

        opening_time = [open_time, close_time]
        return opening_time


def post_daily_close(park):
    date = datetime.datetime.now().date()
    park_id = check_park(park=park)
    date_list = Daily_close.query.filter_by(date=date).filter_by(park=park_id).all()
    if len(date_list) != 0:
        pass
    else:
        close_list = get_close_list_day(park=park)
        for name in close_list:
            attractions = Attraction.query.filter_by(name=name).all()
            if len(attractions) == 0:
                new_attraction = Attraction(name=name, park=park_id)
                db.session.add(new_attraction)
                db.session.commit()
                attractions = Attraction.query.filter_by(name=name).all()
            
            attraction = attractions[0]
            name_id = attraction.id
            new_data = Daily_close(name_id=name_id, date=date, park=park_id)
            db.session.add(new_data)
            db.session.commit()


def post_wait_time(park):
    now = datetime.datetime.now()
    now = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute)
    time = now.time()
    date = now.date()
    data_list = get_wait_time(park=park)
    park_id = check_park(park=park)
    for data in data_list:
        name = data['name']
        attractions = Attraction.query.filter_by(name=name).all()
        if len(attractions) == 0:
            new_attraction = Attraction(name=name, park=park_id)
            db.session.add(new_attraction)
            db.session.commit()
            attractions = Attraction.query.filter_by(name=name).all()
        
        attraction = attractions[0]
        name_id = attraction.id
        new_data = Time_Data(name_id=name_id, tag_id=data['tag_id'], wait_time=data['wait_time'], pass_time=data['pass_time'], date=date, time=time, park=park_id)
        db.session.add(new_data)
        db.session.commit()


def post_show_list(park):
    date = datetime.datetime.now().date()
    park_id = check_park(park=park)
    date_list = Show_data.query.filter_by(date=date).filter_by(park=park_id).all()
    if len(date_list) != 0:
        pass
    else:
        data_list = get_show_list(park=park)
        for data in data_list:
            name = data['name']
            shows = Show.query.filter_by(name=name).all()
            if len(shows) == 0:
                new_show = Show(name=name, park=park_id)
                db.session.add(new_show)
                db.session.commit()
                shows = Show.query.filter_by(name=name).all()
            
            show = shows[0]
            name_id = show.id
            new_data = Show_data(name_id=name_id, time=data['time'], date=date, park=park_id)
            db.session.add(new_data)
            db.session.commit()
