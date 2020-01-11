from flask import render_template, session
from . import app

@app.route('/')
def home():
  return render_template(
    'index.html',
    current_user = session.get('current_user'),
    username = session.get('username')
  )
