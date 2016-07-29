from rechercheparmot import *
import pymongo
client = pymongo.MongoClient('localhost', 27017)
db = client.TweetAnalysis
db = pymongo.MongoClient().Tweetsdb

def bestTweet(topic):
    connect(topic)
    x = 0
    #db.Tweetfind.drop()
    statistics=db.Tweetfind.aggregate([  { "$group": { "_id": "$sentimentRating", "tagCount": {"$sum": 1} }},{ "$sort": {"tagCount": 1 }}, { "$limit": 6 }])
    
    liste = []
    for s in statistics:

        x = s['_id']
        query={ 'sentimentRating' : x }
        projection={"_id":0,"sentimentRating":1,'text':1}
        cursor = db.Tweetfind.find(query, projection)
        for k in cursor:
            liste.append(k)
    return liste
