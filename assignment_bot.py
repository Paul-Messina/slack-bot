import slack
import os
# Import Flask
from flask import Flask
# Handles events from Slack
from slackeventsapi import SlackEventAdapter

# Configure your flask application
app = Flask(__name__)

# Configure SlackEventAdapter to handle events
slack_event_adapter = SlackEventAdapter(os.getenv('SIGNING_SECRET'),'/slack/events',app)

# Using WebClient in slack, there are other clients built-in as well !!
client = slack.WebClient(token=os.getenv('SLACK_TOKEN'))

# connect the bot to the channel in Slack Channel
# client.chat_postMessage(channel='#bot-test-channel', text='Assignment Bot Test')

# Get Bot ID
BOT_ID = client.api_call("auth.test")['user_id']

# handling Message Events
@slack_event_adapter.on('message')
def message(payload):
    print(payload)
    event = payload.get('event',{})
    channel_id = event.get('channel')
    user_id = event.get('user')
    question = event.get('text')
    if BOT_ID != user_id:
      if '?' in question:
        client.chat_postMessage(channel=channel_id, text=question)

# Run the webserver micro-service
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0',port=5000)