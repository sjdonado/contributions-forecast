from flask import render_template
from . import app

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/template')
def template():
  return render_template('index.html')