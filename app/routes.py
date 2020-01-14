import json
from flask import render_template, session, Blueprint, redirect
from .services import forecast
from . import logger

main_bp = Blueprint('main_bp', __name__,
                    template_folder='templates',
                    static_folder='static')

@main_bp.route('/')
def index():
  weeks = session.get('current_user')['weeks'] if session.get('current_user') else None
  username = session.get('username') if session.get('username') else ''
  return render_template(
    'index.html',
    current_user = session.get('current_user'),
    username = username,
    weeks = json.dumps(weeks),
  )

@main_bp.route('/forecast')
def forecast_caller():
  weeks = session.get('current_user')['weeks'] if session.get('current_user') else None
  data = forecast.execute(weeks)
  return json.dumps(data)

