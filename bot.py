import slack
import os
from pathlib import Path
from dotenv import load_dotenv

#better to load it from the .env file because it's sensitive info
env_path = Path(',') / '.env'
load_dotenv()

print(os.environ['SLACK_TOKEN'])

client = slack.WebClient(token=os.environ['SLACK_TOKEN']);

client.chat_postMessage(channel='#test', text="Hello world")