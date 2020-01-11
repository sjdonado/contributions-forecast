import os
import requests

from flask import redirect, request
from . import app

client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']

@app.route('/oauth/authorize')
def oauth_authorize():
  print(request.values)
  username = request.values.get('username')
  return redirect("https://github.com/login/oauth/authorize?client_id={}&login={}&scope=user&state={}"
    .format(client_id, username, 'juan'))

@app.route('/oauth/callback')
def oauth_callback():
  code = request.values.get('code')
  if code is None:
    return ('Code is required', 400)

  response = requests.post(url = "https://github.com/login/oauth/access_token", data = {
    'client_id': client_id,
    'client_secret': client_secret,
    'code': code,
  })

  app.logger.info(response)
  app.logger.info(response.text)

  return 'Ok'

