
# coding: utf-8

# In[ ]:


import tweepy
import csv
import pandas as pd

api_key = 'csenfG8y4VyDpf3BMruZxVBjg'
api_secret = 'TGFqKeXMPJwwj5tQfcBoguCytQ3TtgQw4Xr8BHHw1OUtdk4Tni'
token = '2148411505-BfBRloIT0BRmt5yKoOIPYaHU7YSXoyJ4mlHPrZf'
token_secret = '2ZD1KKL3my4GZDdVLQB4ss8fScYLT7A0UV4AYZur3XD21'

auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(token, token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

csvFile = open('tweets2.csv', 'a')
csvWriter = csv.writer(csvFile)

for tweet in tweepy.Cursor(api.search,q="health",count=20000,
                           wait_on_rate_limit=True,tweet_mode='extended',
                           lang="en",since="2019-03-17").items():
    if (not tweet.retweeted) and ('RT @' not in tweet.full_text):
        csvWriter.writerow([tweet.full_text.encode('utf-8')])

csvFile.close()

