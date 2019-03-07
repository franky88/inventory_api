from flask import Blueprint, render_template
from flask.views import MethodView
from hubeapp.models.models import Item

mod = Blueprint('site', __name__)

@mod.route('/home')
def home():
    all_item = Item.query.all()
    return render_template('home.html', items=all_item)