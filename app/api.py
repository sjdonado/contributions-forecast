import requests
import hashlib
import re
import json

from flask import redirect, request, session

from . import queries
from . import app
from config import Config

client_id = Config.CLIENT_ID
client_secret = Config.CLIENT_SECRET

def get_contributions(access_token):
  headers = { 'Authorization': "bearer {}".format(access_token) }

  data = {
    "query": queries.get_contributions,
    "variables": {
      "username": session.get('username'),
    },
  }

  app.logger.info(data)
  app.logger.info(headers)
  return requests.post(url = "https://api.github.com/graphql", json = data, headers = headers)


@app.route('/oauth/authorize', methods=['GET'])
def oauth_authorize():
  username = request.values.get('username')
  if username is None:
    return ('Username is required', 400)

  session['username'] = username
  session['state'] = hashlib.sha1(username.encode()).hexdigest()

  return redirect("https://github.com/login/oauth/authorize?client_id={}&login={}&scope=user&state={}"
    .format(client_id, username, session.get('state')))

@app.route('/oauth/callback', methods=['GET'])
def oauth_callback():
  code = request.values.get('code')
  if code is None:
    return ('Code is required', 400)

  state = request.values.get('state')
  if state is None or state != hashlib.sha1(session.get('username').encode()).hexdigest():
    return('State is invalid', 400)

  auth_response = requests.post(url = "https://github.com/login/oauth/access_token", data = {
    'client_id': client_id,
    'client_secret': client_secret,
    'code': code,
  })

  if auth_response.status_code != 200 or 'access_token' not in auth_response.text:
    return('Access token is required', 400)

  access_token = re.findall(r"^access_token=([\w]*)&", auth_response.text)[0]

  contributions_response = get_contributions(access_token)
  if contributions_response.status_code != 200:
    return('Get contributions query failed', 500)

  user_data = contributions_response.json()['data']['user']

  session['current_user'] = {
    'name': user_data['name'],
    'total_contributions': user_data['contributionsCollection']['contributionCalendar']['totalContributions'],
  }
  session['weeks'] = json.dumps(user_data['contributionsCollection']['contributionCalendar']['weeks'])
  # app.logger.info(session.get('current_user'))

  return redirect('/')

