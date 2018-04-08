import tweepy
import json
import csv
from textblob import TextBlob
from operator import itemgetter        


#auth Twitter Api
consumer_key = 'xxxxxxxx'
consumer_secret = 'xxxxxxxx'

access_token= 'xxxxxxxx'
access_token_secret= 'xxxxxxxx'

auth= tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#api=tweepy.API(auth)
#response_tweets = api.search('#transperth')

query = 'transperth -filter:retweets'
max_tweets = 500
response_tweets = [status for status in tweepy.Cursor(api.search, q=query).items(max_tweets)]

#header = strjson.keys();
#defining the headers for CSV
header = ['created_at','id','text','tweepy_sent_polarity','tweepy_sent_subjectivity','link','tweepy_language']

with open('output.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=header,extrasaction='ignore')
    writer.writeheader()
    for tweets in response_tweets:
        print(tweets.id)
        enrichtweet = tweets._json
        #improving Date format
        cleantext = ' '.join(tweets.text.split())
        enrichtweet['text'] = cleantext.replace(",","--")
        enrichtweet['created_at'] = str(tweets.created_at)
        try:
            enrichtweet['link'] = tweets.entities['urls'][0]['url']
        except IndexError:
            print("NO_LINK")
            enrichtweet['link'] = 'NO_LINK'
                    
        tweepy = (TextBlob(tweets.text))
        #enriching data with Tweepy
        enrichtweet['tweepy_sent_polarity'] = tweepy.sentiment.polarity
        enrichtweet['tweepy_sent_subjectivity'] = tweepy.sentiment.subjectivity
        enrichtweet ['tweepy_language']= tweepy.detect_language()
        #writing one line in CSV
        writer.writerow(enrichtweet)