import pandas as pd
import transformers as ppb
import numpy as np
import tweepy 
from tweepy.auth import OAuthHandler
import json
import time

with open("twitter_credentials.json", "r") as file:
    creds = json.load(file)
# Fill the X's with the credentials obtained by 
# following the above mentioned procedure. 
CONSUMER_KEY = creds["CONSUMER_KEY"]
CONSUMER_SECRET = creds["CONSUMER_SECRET"]
ACCESS_KEY = creds["ACCESS_TOKEN"]
ACCESS_SECRET = creds["ACCESS_SECRET"]

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

### INIT MODEL ###
# Pkl_Filename = "Pickle_BERT_Model.pkl"
# model_class, tokenizer_class, pretrained_weights = (ppb.DistilBertModel, ppb.DistilBertTokenizer, 'bert_files')

# tokenizer = tokenizer_class.from_pretrained(pretrained_weights)
# model = model_class.from_pretrained(pretrained_weights)

# with open(Pkl_Filename, 'rb') as file:  
#     lr_clf = pickle.load(file)

### FEATURIZE TWEET FROM TWITTER ###
# def predict(tweet):
#     print("The tweet that's coming through is {}".format(tweet))
#     tweet_list = [tweet]
#     df = pd.DataFrame(tweet_list)
#     df.columns = [1]

#     df[1] = df[1].replace('RT', '')
#     df[1] = df[1].replace(r'^https?:\/\/.*[\r\n]*', '')

#     tokenized = df[1].apply(lambda x: tokenizer.encode(str(x), add_special_tokens=True))

#     max_len = 0
#     for i in tokenized.values:
#         if len(i) > max_len:
#             max_len = len(i)

#     padded = np.array([i + [0]*(max_len-len(i)) for i in tokenized.values])

#     attention_mask = np.where(padded != 0, 1, 0)

#     input_ids = torch.tensor(padded[:])  
#     attention_mask = torch.tensor(attention_mask[:])

#     with torch.no_grad():
#         last_hidden_states = model(input_ids.to(torch.int64), attention_mask=attention_mask)

#     features = last_hidden_states[0][:,0,:].numpy()

#     return lr_clf.predict(features[0, np.newaxis])[0]

# def reply_to_tweets():
#     print('retrieving and replying to tweets...', flush=True)
#     for mention in tweepy.Cursor(api.search, q="@unbiased_bot").items(5):
#         print(str(mention.id) + ' - ' + mention.text, flush=True)
#         reply_to_tweet = str(api.get_status(mention.in_reply_to_status_id).text)

#         print('predicting...', flush=True)
#         predicted = predict(reply_to_tweet)
#         predicted_in_tweet = '' 
#         if predicted == 'HillaryClinton':
#             predicted_in_tweet = "left"
#         else:
#             predicted_in_tweet = "right"
        
#         print('responding back...', flush=True)
#         try:
#             if "#" in reply_to_tweet:
#                 hash_num = reply_to_tweet.find("#")
#                 space_num = reply_to_tweet[hash_num:].find(' ')
#                 if space_num != -1:
#                     hashtag_to_search = reply_to_tweet[hash_num + 1: hash_num + space_num]
#                 else:
#                     hashtag_to_search = reply_to_tweet[hash_num + 1:]
#                 api.update_status('@' + mention.user.screen_name +
#                         ' Hey there! The tweet you are currently looking at is quite a ' + predicted_in_tweet + ' tweet. If you want to take a look at more tweets with the whole left and right predicament, here ya go: http://127.0.0.1:5000/tweets?searchinput=' + hashtag_to_search, mention.id)
#             else:
#                 api.update_status('@' + mention.user.screen_name +
#                         ' Hey there! The tweet you are currently looking at is quite a ' + predicted_in_tweet + ' tweet. If you want to take a look at more tweets with the whole left and right predicament, here ya go: http://127.0.0.1:5000/', mention.id)
#         except:
#             pass


df = pd.read_csv('incidents_speech.csv')
speak_output = ''
i=1

for output in reversed(df['Speech Output']):
    try:
        speak_output = str(i) + ". " + output
        speak_output = speak_output[:-19]
        print(len(speak_output))
        count = 220
        tweet = " "
        if (len(speak_output) > 220):
            while speak_output[count] != ' ':
                count = count + 1
            tweet = speak_output[:count]
            tweet += " (1/2)"
        else:
            tweet = speak_output
        
        og_tweet = api.update_status(status =tweet, tweet_mode='extended') 
        if(len(speak_output) > count) :
            api.update_status(status=speak_output[count:]+" (2/2)", 
                                    in_reply_to_status_id=og_tweet.id, 
                                    auto_populate_reply_metadata=True)
        time.sleep(30)
        i = i+1
        print(speak_output)
    except tweepy.TweepError as error:
        print(error)


