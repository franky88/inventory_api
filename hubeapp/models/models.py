from flask_sqlalchemy import SQLAlchemy
from hubeapp import app
import os

db = SQLAlchemy(app)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app.config['SECRET_KEY'] = 'thisissecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'hubedb.db')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(60))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)
    active = db.Column(db.Boolean)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.String(20), unique=True)
    item_name = db.Column(db.String(60))
    description = db.Column(db.String(120))
    model = db.Column(db.String(20))
    quantity = db.Column(db.Integer)
    cost = db.Column(db.Float)
    user_id = db.Column(db.Integer)

