import folium, pandas, ast
import pymongo
import pandas as pd
from rechercheparmot import *

client = pymongo.MongoClient('localhost', 27017)
db = client.TweetAnalysis
db = pymongo.MongoClient().Tweetsdb

# get geo data only from rows with non-empty values
#locations = pandas.read_csv('./tweets.csv', usecols=[3]).dropna()
def geomap_col():
    
    
    query={}
    projection={"_id":0,"geo":1,"text":1,"user.screen_name":1,"sentimentRating":1}
    cursor = db.Tweets.find(query,projection)
    geos = []
    dic = {}
    map_1 = folium.Map(location=[45.372, -121.6972],
                   zoom_start=2,
                   tiles='Mapbox Bright')
    for a in cursor:
      if a['geo'] != None:
        geos.append(a['geo']['coordinates'])
        dic['place']=a['geo']['coordinates']
        dic['user']=a['user']['screen_name']
        dic['sent']=a['sentimentRating']
        if a['sentimentRating'] > 0.0:
            col = 'blue'
        elif a['sentimentRating'] < 0.0:
            col = 'red'
        else :
            col = 'green'
        folium.Marker(a['geo']['coordinates'],popup=a['user']['screen_name'],icon=folium.Icon(color=col) ).add_to(map_1)

    # initialize and create map
    # add markers
    
   
        
    map_1.save('map_col_all.html')
def geomap_col_mot(text):
    connect(text)
    
    
    query={}
    projection={"_id":0,"geo":1,"text":1,"user.screen_name":1,"sentimentRating":1}
    cursor = db.Tweetfind.find(query,projection)
    geos = []
    dic = {}
    map_1 = folium.Map(location=[45.372, -121.6972],
                   zoom_start=2,
                   tiles='Mapbox Bright')
    for a in cursor:
      if a['geo'] != None:
        geos.append(a['geo']['coordinates'])
        dic['place']=a['geo']['coordinates']
        dic['user']=a['user']['screen_name']
        dic['sent']=a['sentimentRating']
        if a['sentimentRating'] > 0.0:
            col = 'blue'
        elif a['sentimentRating'] < 0.0:
            col = 'red'
        else :
            col = 'green'
        folium.Marker(a['geo']['coordinates'],popup=a['user']['screen_name'],icon=folium.Icon(color=col) ).add_to(map_1)

    # initialize and create map
    # add markers
    
   
        
    map_1.save('map_col_mot.html')
           

