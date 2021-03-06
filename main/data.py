from main.models import Attraction, Time_Data, Daily_close, Show, Show_data
import pandas as pd

def get_name(name_ids):
    names = []
    attractions = Attraction.query.all()
    for name_id in name_ids:
        for attraction in attractions:
            if name_id == attraction.id:
                if attraction.alias != None:
                    names.append(attraction.alias)
                else:
                    names.append(attraction.name)
    return names

def wait_df(data_list, tag):
    if tag == False:
        data_list = [data for data in data_list if data.tag_id == 0]
    elif tag == True:
        data_list = [data for data in data_list if data.tag_id != 0]
    name_ids = [data.name_id for data in data_list]
    names = get_name(name_ids=name_ids)
    wait_times = [data.wait_time for data in data_list]
    times = [data.time for data in data_list]
    
    df = pd.DataFrame([names, wait_times, times], index=['name', 'wait_time', 'time']).T
    df_list = []
    for name, group in df.groupby('time'):
        w_l = [f'{name.hour}:{name.minute}']
        for w in list(group['wait_time']):
            w_l.append(w)
        df_list.append(w_l)

    names2 = sorted(set(names), key=names.index)
    name_list = ['time']
    for name in names2:
        name_list.append(name)

    df = pd.DataFrame(df_list, columns=name_list).set_index('time')
    return df

def pass_df(data_list):
    data_list = [data for data in data_list if data.tag_id != 0]
    name_ids = [data.name_id for data in data_list]
    names = get_name(name_ids=name_ids)
    pass_times = [data.pass_time for data in data_list]
    times = [data.time for data in data_list]
    
    df = pd.DataFrame([names, pass_times, times], index=['name', 'pass_time', 'time']).T
    df_list = []
    for name, group in df.groupby('time'):
        w_l = [f'{name.hour}:{name.minute}']
        for w in list(group['pass_time']):
            w_l.append(w)
        df_list.append(w_l)

    names2 = sorted(set(names), key=names.index)
    name_list = ['time']
    for name in names2:
        name_list.append(name)

    df = pd.DataFrame(df_list, columns=name_list).set_index('time')
    return df

def get_data(park_id, date):
    data_list = Time_Data.query.filter_by(date=date).filter_by(park=park_id).all()

    today_closes = Daily_close.query.filter_by(date=date).filter_by(park=park_id).all()
    closes = [Attraction.query.get(close.name_id).name for close in today_closes]

    close_ids = [close.name_id for close in today_closes]
    data_list = [data for data in data_list if data.name_id not in close_ids]

    notag_df = wait_df(data_list=data_list, tag=False)
    tag_df = wait_df(data_list=data_list, tag=True)
    p_df = pass_df(data_list=data_list)
    return [closes, notag_df, tag_df, p_df]

def get_shows(date, park_id):
    today_shows = Show_data.query.filter_by(date=date).filter_by(park=park_id).all()
    shows = [[Show.query.get(show.name_id).name, show.time] for show in today_shows]
    return shows