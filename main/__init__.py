from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///wait_time.db"
    return app

app = create_app()
db = SQLAlchemy(app)

from main.models import init_table
init_table()

from main import views