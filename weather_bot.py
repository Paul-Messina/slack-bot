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

slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events',app)

slack_client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

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

def create_bigram(word):
  return [word[i] + word[i+1] for i in range(len(word)-1)]

def get_similarity_ratio(word1, word2):
  word1, word2 = word1.lower(), word2.lower()
  common = []
  bigram1, bigram2 = create_bigram(word1), create_bigram(word2)
  for i in range(len(bigram1)):
    try:
      cmn_elt = bigram2.index(bigram1[i])
      common.append(bigram1[i])
    except:
      continue

  return len(common)/max(len(bigram1), len(bigram2))

def nlp(city_name, database={'toronto', 'paris', 'tokyo', 'vancouver', 'shanghai'}):
  max_sim = 0.0
  most_sim_word = 'toronto'

  for data_word in database:
    cur_sim = get_similarity_ratio(city_name, data_word)
    if cur_sim > max_sim:
      max_sim = cur_sim
      most_sim_word = data_word

  return most_sim_word

@slack_event_adapter.on('message')
def printWeather(payload):
  print(payload)
  event = payload.get('event',{})
  channel_id = event.get('channel')
  user_id = event.get('user')
  text2 = event.get('text')
  o = getOvercast(nlp(text2))
  t = getTemp(nlp(text2))
  p = nlp(text2).capitalize()
  if BOT_ID !=user_id:
    slack_client.chat_postMessage(channel=channel_id, text='Detected City: ' + str(p))
    slack_client.chat_postMessage(channel=channel_id, text='The temperature is: ' + str(t) + ' °c')
    slack_client.chat_postMessage(channel=channel_id, text='Overcast: ' + str(o))

# Run the webserver micro-service
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)