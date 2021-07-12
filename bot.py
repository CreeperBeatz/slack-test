import slack
import os
import stringformatter
from pathlib import Path
from dotenv import load_dotenv
from slackeventsapi import SlackEventAdapter
from flask import Flask

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
    if 'hello' in text and user_id != BOT_ID:
        print_hello(channel_id=channel_id, user = user_name)

def print_hello(channel_id, user):
    client.chat_postMessage(
        channel = channel_id,
        text = f'Hello {util.getFirstName(user)}! I\'m slacky!'
    )


if __name__ == "__main__": # if we ran this file directly (not with include), run the web server
    app.run(debug=True, port=5000)
