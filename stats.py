import nltk, pandas
from nltk.corpus import stopwords
from nltk import FreqDist
import matplotlib.pyplot as plt
import pymongo
from rechercheparmot import *
client = pymongo.MongoClient('localhost', 27017)
db = client.TweetAnalysis
db = pymongo.MongoClient().Tweetsdb

def statistics_simple():
    query={}
    projection={"_id":0,"sentimentRating":1,"user.lang":1}
    cursor = db.Tweets.find(query,projection)
    texts = pandas.Series(list(cursor))
    tokens = []
    n=0
    p=0
    d=0
    # strip words of punctuation marks
    
    for sentimentRating in texts.values:
        if sentimentRating['user']['lang'] in ['en','fr']:
            
            if sentimentRating['sentimentRating']<0:
                d=d+1
            if sentimentRating['sentimentRating']==0:
                n=n+1
            if sentimentRating['sentimentRating']>0:
                p=p+1
            
    name = ['Positive','Neutre','Negative']
    data = [p,n,d]
    s=(p+d+n)
    a=(float(p)/float(s))*100
    b=(float(d)/float(s))*100
    c=(float(n)/float(s))*100
    explode=(0,0,0)
    plt.pie(data, explode=explode, labels=name,autopct='%1.1f%%',startangle=90)
    plt.title('Sentiments des Tweets')
    plt.show()

def statistics_word(topic):
    connect(topic)
    
    query={}
    projection={"_id":0,"sentimentRating":1,"user.lang":1}
    cursor = db.Tweetfind.find(query,projection)

    texts = pandas.Series(list(cursor))
    tokens = []

    n=0
    p=0
    d=0
    # strip words of punctuation marks
    for sentimentRating in texts.values:
        if sentimentRating['user']['lang'] in ['en','fr']:
            
            if sentimentRating['sentimentRating']<0:
                d=d+1
            if sentimentRating['sentimentRating']==0:
                n=n+1
            if sentimentRating['sentimentRating']>0:
                p=p+1
            
    name = ['Positive','Neutre','Negative']
    data = [p,n,d]
    s=(p+d+n)
    a=(float(p)/float(s))*100
    b=(float(d)/float(s))*100
    c=(float(n)/float(s))*100
    explode=(0,0,0)
    plt.pie(data, explode=explode, labels=name,autopct='%1.1f%%',startangle=90)
    plt.title('Sentiments des Tweets')
    plt.show()
