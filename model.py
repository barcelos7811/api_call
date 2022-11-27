from flask import Flask, request, jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
import psycopg2
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/call'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200))

    def __init__(self, description):
        self.description = description