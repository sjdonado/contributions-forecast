import json
from flask import render_template, session, Blueprint, redirect
from .services import predictor
from . import executor

main_bp = Blueprint('main_bp', __name__,
                    template_folder='templates',
                    static_folder='static')

@main_bp.route('/')
def index():
  weeks = session.get('current_user')['weeks'] if session.get('current_user') else None

  return render_template(
    'index.html',
    current_user = session.get('current_user'),
    username = session.get('username') if session.get('username') else '',
    weeks = json.dumps(weeks),
    prediction_status = session.get('prediction_status'),
    prediction = json.dumps(session.get('prediction'))
  )

@main_bp.route('/prediction')
def prediction():
  if session.get('prediction_status') is None:
    weeks = session.get('current_user')['weeks'] if session.get('current_user') else None
    session['prediction_status'] = 'Sent'

    executor.submit(call_predictor, weeks)

  return redirect('/')

def call_predictor(weeks):
  if weeks:
    session['prediction_status'] = 'Training...'
    session['prediction'] = json.dumps(predictor.execute(weeks))
    session['prediction_status'] = 'Completed'
