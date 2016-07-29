import nltk
from pymongo import MongoClient
import pymongo
def looking(x,y):
    tokens = nltk.word_tokenize(x)
    i=0
    i=len(tokens)
    c=0
    while c<=i-1:
        if tokens[c]==y:
            return True
            break
        else:
            c=c+1
    return False
def connect(y):

    client = MongoClient('localhost', 27017)
    db = client.TweetAnalysis
    db = pymongo.MongoClient().Tweetsdb
    query={}
    projection={"user.text":0}
    if y == '0661168090':
        tweets=db.Tweets.find(query,projection)
        db.Tweetfind.drop()
        for sentences in tweets:
            db.Tweetfind.insert(sentences)

    elif y != '0661168090':       
        tweets=db.Tweets.find(query,projection)
        db.Tweetfind.drop()
        for sentences in tweets:
            x=sentences['text'].lower() 
            z=looking(x,str(y).lower())
            if z==True:
                db.Tweetfind.insert(sentences)

