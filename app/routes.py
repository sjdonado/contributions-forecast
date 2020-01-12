import json
from flask import render_template, session, Blueprint
from .services import predictor

main_bp = Blueprint('main_bp', __name__,
                    template_folder='templates',
                    static_folder='static')

@main_bp.route('/')
def index():
  session['username'] = ''
  return render_template(
    'index.html',
    current_user = session.get('current_user'),
    username = session.get('username'),
    weeks = json.dumps(session.get('current_user')['weeks'] if session.get('current_user') else None)
  )

@main_bp.route('/calculate')
def calculate_prediction():
  weeks = session.get('current_user')['weeks'] if session.get('current_user') else None
  predicted_days = predictor.by_weeks(weeks)
  # '' if session.get('username') is None else session.get('username')
  return render_template(
    'index.html',
    current_user = session.get('current_user'),
    username = session.get('username'),
    weeks = json.dumps(weeks),
    predicted_days = json.dumps(predicted_days)
  )
