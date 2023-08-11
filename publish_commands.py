#!/usr/bin/python
# this script sets the commands for a Discord application
# run this with Python 3.11

import requests
from public_key import AUTH_TOKEN, APPLICATION_ID
# AUTH_TOKEN is bot secret key, formatted like 'Bot <base64 stuff>.<stuff>.<stuff>_<stuff>-<stuff>'
# APPLICATION_ID is bot application ID

url = f"https://discord.com/api/v10/applications/{APPLICATION_ID}/commands"

# This is an example CHAT_INPUT or Slash Command, with a type of 1
json = {
    "name": "neotrias",
    "type": 1,
    "description": "Talk to the neotrias server",
    "options": [
        {
            "name": "start",
            "description": "Start the server",
            "type": 1,
            "required": False,
        },
        {
            "name": "stop",
            "description": "Stop the server",
            "type": 1,
            "required": False,
        },
        {
            "name": "whitelist",
            "description": "Add player to the server's whitelist",
            "type": 1,
            "required": False,
            "options": [
                {
                    "name": "username",
                    "description": "The username of the player to add to the whitelist",
                    "type": 3,
                    "required": True
                }
            ],
        }
    ]
}

# For authorization, you can use either your bot token
headers = {
    "Authorization": AUTH_TOKEN
}

r = requests.post(url, headers=headers, json=json)

print(r.text)
print(r.status_code)
