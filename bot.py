import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from slackeventsapi import SlackEventAdapter
from flask import Flask

#better to load it from the .env file because it's sensitive info
env_path = Path(',') / '.env'
load_dotenv()

app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(
    os.environ['SIGNING_SECRET'],'/slack/events', app)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

#response = client.chat_postMessage(channel='#test', text="Hello world!")

# assert response["ok"]
# assert response["message"]["text"] == "Hello world!"

if __name__ == "__main__":
    app.run(debug=True, port=5000)