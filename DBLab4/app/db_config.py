from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient

import os

db_main_host = os.getenv('POSTGRES_HOST')
db_main_port = int(os.getenv('POSTGRES_PORT'))
db_main_name = os.getenv('POSTGRES_DB')
db_main_user = os.getenv('POSTGRES_USER')
db_main_password = os.getenv('POSTGRES_PASSWORD')

db_mongo_host = os.getenv('MONGO_HOSTNAME')
db_mongo_port = int(os.getenv('MONGO_PORT'))
db_mongo_name = os.getenv('MONGO_INITDB_DATABASE')
db_mongo_user = os.getenv('MONGO_INITDB_ROOT_USERNAME')
db_mongo_password = os.getenv('MONGO_INITDB_ROOT_PASSWORD')

app = Flask(__name__)
app.secret_key = 'key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{}:{}@{}:{}/{}'.format(db_main_user, db_main_password, db_main_host, db_main_port, db_main_name)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

mongo_client = MongoClient('mongodb://{}:{}@{}:{}'.format(db_mongo_user, db_mongo_password, db_mongo_host, db_mongo_port))
mongo_db = mongo_client[db_mongo_name]


