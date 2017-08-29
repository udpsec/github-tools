#!/usr/bin/env python

# send github starred repos to pinboard
# Get info about pinboard token here:
#   https://blog.pinboard.in/2012/07/api_authentication_tokens/

import sys

import requests

if len(sys.argv) != 3:
    print"Usage: {0} [github username] [pinboard token]".format(sys.argv[0])
    sys.exit(-1)

username = sys.argv[1]
token = sys.argv[2]


GH_URL = 'https://api.github.com/users/{username}/starred'
ADD_URL = 'https://api.pinboard.in/v1/posts/add'
GET_URL = 'https://api.pinboard.in/v1/posts/get'


starred = requests.get(GH_URL.format(username=username)).json()

pb_session = requests.Session()
pb_session.params = {'auth_token': token}


for repo in starred:
    url = repo.get('html_url')
    exists = pb_session.get(GET_URL, params={'url': url})
    exists.raise_for_status()

    if exists.status_code != 200:
        print("Bad response")
        continue

    if url not in exists.text:
        params = {'url': url,
                  'description': repo.get('full_name'),
                  'extended': repo.get('description'),
                  'tags': 'github,starred'}
        update = pb_session.get(ADD_URL, params=params)
        update.raise_for_status()
        print('Added {0}'.format(repo.get('name')))
