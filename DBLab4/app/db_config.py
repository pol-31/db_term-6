from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
from pymongo import MongoClient

db_main_host: str = "db"
db_main_port: int = 5432
db_main_name: str = "zno_data"
db_main_user: str = "dreamTeam"
db_main_password: str = "dreamTeam"


app = Flask(__name__)
app.secret_key = 'key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dreamTeam:dreamTeam@db:5432/zno_data'
#app.config['MONGO_URI'] = 'mongodb://admin:admin@mongodb:27017/your_mongodb_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

#mongo_db = PyMongo(app)


mongo_client = MongoClient('mongodb://admin:admin@mongodb:27017')
mongo_db = mongo_client['your_mongodb_database']


