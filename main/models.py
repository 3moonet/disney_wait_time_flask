from main import db

class Attraction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    alias = db.Column(db.String)
    park = db.Column(db.Integer, nullable=False) # tdl=0, tds=1

class Time_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_id = db.Column(db.Integer, nullable=False)
    tag_id = db.Column(db.Integer, nullable=False)
    wait_time = db.Column(db.String)
    pass_time = db.Column(db.String)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    park = db.Column(db.Integer, nullable=False) # 0 or 1

class Opening_time(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    open_time = db.Column(db.Time, nullable=False)
    close_time = db.Column(db.Time, nullable=False)
    park = db.Column(db.Integer, nullable=False) # 0 or 1

class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    park = db.Column(db.Integer, nullable=False) # 0 or 1

class Show_data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_id = db.Column(db.Integer, nullable=False)
    time = db.Column(db.String)
    date = db.Column(db.Date, nullable=False)
    park = db.Column(db.Integer, nullable=False) # 0 or 1

class Daily_close(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    park = db.Column(db.Integer, nullable=False) # 0 or 1

# class Monthly_close(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name_id = db.Column(db.Integer, nullable=False)
#     date = db.Column(db.String, nullable=False)
#     month = db.Column(db.Date, nullable=False)

def init_table():
    db.create_all()