import nltk, pandas
from nltk.corpus import stopwords
from nltk import FreqDist
import pymongo
import pandas as pd
from rechercheparmot import *
client = pymongo.MongoClient('localhost', 27017)
db = client.TweetAnalysis
db = pymongo.MongoClient().Tweetsdb

def freqgen():
  # get english stopwords
  stopen = stopwords.words('english')
  stopfr = stopwords.words('french')
  stopsp = stopwords.words('spanish')

  query={}
  projection={"text":1}

  cursor = db.Tweets.find(query,projection)

  texts = pandas.Series(list(cursor))
  tokens = []

  for text in texts.values:
    tokens.extend([word.lower().strip(':,#."-\'') for word in text['text'].split()])
  filtered_tokens=[]
  st = ['it\'s','haven\'t','can\'t','don\'t','i\'m','i\'ve','i\'ll','i\'d','#','e','@','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','rt','(',')']
  for word in tokens:
    try:
      if (not word.decode('utf-8') in stopen) and (not word.decode('utf-8') in stopfr)and (not word.decode('utf-8') in stopsp):
        if not word in st:  
          filtered_tokens.append(word.decode('utf-8'))
    except :
      pass
  freq_dist = nltk.FreqDist(filtered_tokens)
  print type(freq_dist)
  return freq_dist
#print freq_dist.plot(25)
def freqgen_word(word):
  connect(word)
  # get english stopwords
  stopen = stopwords.words('english')
  stopfr = stopwords.words('french')
  stopsp = stopwords.words('spanish')

  query={}
  projection={"text":1}

  cursor = db.Tweetfind.find(query,projection)

  texts = pandas.Series(list(cursor))
  tokens = []

  for text in texts.values:
    tokens.extend([word.lower().strip(':,#."-\'') for word in text['text'].split()])
  filtered_tokens=[]
  st = ['it\'s','haven\'t','can\'t','don\'t','i\'m','i\'ve','i\'ll','i\'d','#','e','@','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','rt','(',')']
  for word in tokens:
    try:
      if (not word.decode('utf-8') in stopen) and (not word.decode('utf-8') in stopfr)and (not word.decode('utf-8') in stopsp):
        if not word in st:  
          filtered_tokens.append(word.decode('utf-8'))
    except :
      pass
  freq_dist = nltk.FreqDist(filtered_tokens)
  print type(freq_dist)
  return freq_dist
