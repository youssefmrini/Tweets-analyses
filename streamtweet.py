import tweepy
import sys
import json
import urllib
import urllib2
import pymongo
import yaml
from sentiment import *
from tweepy import OAuthHandler, Stream, API
from tweepy.streaming import StreamListener
#consumer_key="R72qfP4wzdJnh4kVBtiYn3i8S"
#consumer_secret="NHJuLFDsbu6FsLinRNl9lq3uoNhBlWtB3CByAD21Ejk4O42BuO"

#access_token="125108625-phrqEmj9Mk5y8fQB2kgc9bCeZmwATa8aujLsGrJA"
#access_token_secret="qGRtme7HTMZFqRmcSZ60ngX927oZYesV23iyQwQ3fBdvk"
consumer_key="UQ1vN4kWQgfzxN282HYrE7P9B"
consumer_secret="RD1j0kiy68Ot1gG5DuXBQ7JSaSNDZH2YtQTRrqP2kllch55lFN"

access_token="125108625-xpm6y3tQWrrKdBqc723N9pzweNhM5pOZ6zBbKXjO"
access_token_secret="UYl7MVlo7lpazz0QGbxoKqNkTzSvzmOZd1pEyKJvIWhN7"


client = pymongo.MongoClient('localhost', 27017)
db = client.TweetAnalysis

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = API(auth)

def getsentiment(text):
    splitter = Splitter()
    postagger = POSTagger()
    splitted_sentences = splitter.split(text)
    pos_tagged_sentences = postagger.pos_tag(splitted_sentences)
    dicttagger = DictionaryTagger([ 'dicts/positive.yml', 'dicts/negative.yml', 'dicts/inc.yml', 'dicts/dec.yml', 'dicts/inv.yml'])
    dict_tagged_sentences = dicttagger.tag(pos_tagged_sentences)
    return sentiment_score(dict_tagged_sentences)




    
class CustomListener(StreamListener):
    def __init__(self, api):
        self.api = api
        super(tweepy.StreamListener, self).__init__()
        self.db = pymongo.MongoClient().Tweetsdb

    def on_status(self, tweet):
        data = tweet._json
        print data['text']
        sent = getsentiment(data['text'])
        print sent
        data['sentimentRating'] = sent
        self.db.Tweets.insert(data)



    def on_error(self, status):
        print >> sys.stderr, 'Error: ', status
        return True

    def on_timeout(self):
        print >> sys.stderr, 'Stream timeout'
        return True
while True:
    try:
        listen = Stream(auth, CustomListener(api))
        listen.filter(locations=[-180,-90,180,90])
        #listen.filter(track = ['the'])

    except:
        pass
