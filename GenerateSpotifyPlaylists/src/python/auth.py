import random
import string

import urllib.parse as urlparse
from flask import Flask, redirect

import os

app = Flask(__name__)

client_id = os.environ.get("CLIENT_ID")
redirect_uri = 'http://127.0.0.1:5000'

def generateRandomString(length):
    letters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(letters) for _ in range(length))
    return random_string

@app.route('/login')
def login():
    state = generateRandomString(16)
    scopes = 'user-read-private user-read-email'

    spotify_authorize_url = 'https://accounts.spotify.com/authorize'
    query_params = {
        'response_type': 'code',
        'client_id': client_id,
        'scope': scopes,
        'redirect_uri': redirect_uri,
        'state': state,
    }
    
    redirect_url = spotify_authorize_url + '?' + urlparse.urlencode(query_params)

    return redirect(redirect_url)

if __name__ == '__main__':
    app.run()
