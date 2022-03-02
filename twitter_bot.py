import pandas as pd
import numpy as np
import tweepy 
from tweepy.auth import OAuthHandler
import json
import time

with open("twitter_credentials.json", "r") as file:
    creds = json.load(file)

CONSUMER_KEY = creds["CONSUMER_KEY"]
CONSUMER_SECRET = creds["CONSUMER_SECRET"]
ACCESS_KEY = creds["ACCESS_TOKEN"]
ACCESS_SECRET = creds["ACCESS_SECRET"]

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

def tweet(df, date):
    speak_output = ''
    df = df[df['Date'] == "2/{}/2021".format(date)]

    i = 1
    
    announce = "📣 PSA: THE NEXT {} TWEETS ARE FOR INCIDENTS ON 2/{}/2021".format(len(df), date)
    announce_tweet = api.update_status(status = announce, tweet_mode='extended') 

    for output in (df['Speech Output']):
        try:
            speak_output = str(i) + ". " + output
            count = 220
            tweet = " "
            if (len(speak_output) > 220):
                while speak_output[count] != ' ':
                    count = count + 1
                tweet = speak_output[:count]
                tweet += " (1/2)"
            else:
                tweet = speak_output
            
            print(speak_output, flush=True)
            og_tweet = api.update_status(status = tweet, tweet_mode='extended') 
            if(len(speak_output) > count):
                api.update_status(status=speak_output[count:]+" (2/2)", 
                                        in_reply_to_status_id=og_tweet.id, 
                                        auto_populate_reply_metadata=True)
            time.sleep(5)
            i += 1
        except tweepy.TweepError as error:
            print(error)

df = pd.read_csv('./data/incidents_speech.csv')
date = 23

while True:
    if date == 25:
        break
    tweet(df, date)
    time.sleep(60)

    date += 1
    