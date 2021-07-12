from aiohttp.client import request
import slack
import os
import stringformatter
from pathlib import Path
from dotenv import load_dotenv
from slackeventsapi import SlackEventAdapter
from flask import Flask, Request, Response

#better to load it from the .env file because it's sensitive info
env_path = Path(',') / '.env'
load_dotenv()

app = Flask(__name__) # __name__ - python variable containing the name of the file
slack_events_adapter = SlackEventAdapter(
    os.environ['SIGNING_SECRET'],'/slack/events', app)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call('auth.test')['user_id']

util = stringformatter.StringUtilityFormatter

# Listen to all messages
@slack_events_adapter.on('message')
def message(payload):

    channel_type = payload.get('event').get('channel_type')

    if channel_type == 'channel':
        channel_event(payload.get('event'))
    if channel_type == 'im':
        im_event(payload.get('event'))

@app.route('/start-game', methods=['POST'])
def start_game():
    data = request.form
    channel_id = data.get('channel-id')
    if in_game:
        client.chat_postMessage(channel=channel_id, text = "You are already playing!")
    else:
        client.chat_postMessage(channel=channel_id, text = "You are in the game!")
        in_game = True
    return Response(), 200

@app.route('/end-game', methods=['POST'])
def end_game():
    data = request.form
    channel_id = data.get('channel-id')
    client.chat_postMessage(channel=channel_id, text = "You are no longer playing")
    in_game = False
    return Response(), 200

def channel_event(event):
    print('channel event')
    channel_id = event.get('channel')
    text = event.get('text')
    user_id = event.get('user')
    user_name = client.users_profile_get(user=user_id).get('profile').get('real_name')
    if 'hello' in text and user_id != BOT_ID:
        print_hello(channel_id=channel_id, user = user_name)

def im_event(event):
    print('im event')
    channel_id = event.get('channel')
    text = event.get('text')
    user_id = event.get('user')
    user_name = client.users_profile_get(user=user_id).get('profile').get('real_name')
    if in_game:
        simple_game_result(event)
    else:
        channel_id = event.get('channel')
        text = event.get('text')
        user_id = event.get('user')
        user_name = client.users_profile_get(user=user_id).get('profile').get('real_name')
        if 'hello' in text and user_id != BOT_ID:
            print_hello(channel_id=channel_id, user = user_name)


def print_hello(channel_id, user):
    client.chat_postMessage(
        channel = channel_id,
        text = f'Hello {util.getFirstName(user)}! I\'m slacky!'
    )

def simple_game_greeting(channel_id):
    client.chat_postMessage(channel=channel_id, text = 'Welcome to my game!')
    client.chat_postMessage(channel=channel_id, text = 'Are you a programmer? (Yes/No)')

def simple_game_result(event):
    channel_id = event.get('channel')
    text = event.get('text')
    if text.lower() == 'yes':
        client.chat_postMessage(channel=channel_id, text = 'You\'re on the right place then, fellow programmer!')
        client.chat_postMessage(channel=channel_id, text = "You are no longer playing")
        in_game = False
    elif text.lower() == 'no':
        client.chat_postMessage(channel=channel_id, text = 'Huh, what are you doing here then, if you\'re not a programmer?')
        client.chat_postMessage(channel=channel_id, text = "You are no longer playing")
        in_game = False
    else:
        client.chat_postMessage(channel=channel_id, text = 'Sorry, I didn\'t quite catch that, can you repeat? (Yes/No)')




if __name__ == "__main__": # if we ran this file directly (not with include), run the web server
    app.run(debug=True, port=5000)
