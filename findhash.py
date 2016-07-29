import json
from rechercheparmot import *
import pandas as pd
import matplotlib.pyplot as plt
from tweepy import Stream
from tweepy.streaming import StreamListener
from pymongo import MongoClient
from bson.son import SON
from matplotlib import style
client = MongoClient()
client = MongoClient('mongodb://localhost:27017/')
db = client.Tweetsdb
collection=db.Tweetsdb

    
def findhash():
    a=[]
    b=[]
    
    statistics=db.Tweets.aggregate([ {"$unwind": "$entities.hashtags"}, { "$group": { "_id": "$entities.hashtags.text", "tagCount": {"$sum": 1} }},{ "$sort": {"tagCount": -1 }}, { "$limit": 20 }])
    for s in statistics:
        a.append(s['_id'])
        b.append(s['tagCount'])


    style.use('ggplot')

    web_stats={'hashtag':a,'nombre':b}
    df=pd.DataFrame(web_stats)

    return df

def findhash_word(word):
    connect(word)
    a=[]
    b=[]
    
    statistics=db.Tweetfind.aggregate([ {"$unwind": "$entities.hashtags"}, { "$group": { "_id": "$entities.hashtags.text", "tagCount": {"$sum": 1} }},{ "$sort": {"tagCount": -1 }}, { "$limit": 20 }])
    for s in statistics:
        a.append(s['_id'])
        b.append(s['tagCount'])


    style.use('ggplot')

    web_stats={'hashtag':a,'nombre':b}
    df=pd.DataFrame(web_stats)

    return df 

     


