import requests
import slack
from slackeventsapi import SlackEventAdapter
from flask import Flask
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)

slack_event_adapter = SlackEventAdapter(os.getenv('SIGNING_SECRET'),'/slack/events',app)

slack_client = slack.WebClient(token=os.getenv('SLACK_TOKEN'))

BOT_ID = slack_client.api_call("auth.test")['user_id']

def getOvercast(city_name):
  overcast = ''
  getWeatherAPI = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+ str(city_name) +'&APPID='+ '92f7d5e85438fb4478374efe23fb782d' + '&units=metric')
  x = getWeatherAPI.json()
  if 'weather' in x:
    overcast = x['weather'][0]['main']

  return overcast

def getTemp(city_name):
  temp = ''
  getWeatherAPI = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+ str(city_name) +'&APPID='+ '92f7d5e85438fb4478374efe23fb782d' + '&units=metric')
  x = getWeatherAPI.json()
  temp = x['main']['temp']

  return temp

@slack_event_adapter.on('message')
def printWeather(payload):
  print(payload)
  event = payload.get('event',{})
  channel_id = event.get('channel')
  user_id = event.get('user')
  text2 = event.get('text')
  o = getOvercast(text2)
  t = getTemp(text2)
  if BOT_ID !=user_id:
    slack_client.chat_postMessage(channel=channel_id, text='The temperature is ')
    slack_client.chat_postMessage(channel=channel_id, text=t)
    slack_client.chat_postMessage(channel=channel_id, text='°c')
    slack_client.chat_postMessage(channel=channel_id, text='Overcast: ')
    slack_client.chat_postMessage(channel=channel_id, text=o)

# Run the webserver micro-service
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
    keep_alive()