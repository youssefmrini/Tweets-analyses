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
consumer_key="SuTtAPE1sG5OMoLrzvDqyFGbC"
consumer_secret="iMIxtiWifFy8hdPm7zSXTtCJMaWml2P3lidrnMquaDNNCqOIcb"

access_token="125108625-D3CRq1mRuQuDsCJeVwdl5kRK5dAXKfj29hSKRlIl"
access_token_secret="nqywaW1yjaGCbM0gtTz8A5Uamk0al6611974YT5p7Jfto"

client = pymongo.MongoClient('localhost', 27017)
db = client.TweetAnalysis
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
        if (data['user']['lang'] == 'en' or data['user']['lang'] == 'fr'):
                
            sent = getsentiment(data['text'])
            data['sentimentRating'] = sent
        else :
            data['sentimentRating'] = 0.0
        data['sentimentRating'] = sent
        self.db.Tweets.insert(data)
        print data['text']
        return data['text']



    def on_error(self, status):
        print >> sys.stderr, 'Error: ', status
        return True

    def on_timeout(self):
        print >> sys.stderr, 'Stream timeout'
        return True
while True :
    try:
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = API(auth)
        listen = Stream(auth, CustomListener(api))
        
        listen.filter(locations=[-180,-90,180,90])

    except:
        pass


