import folium, pandas, ast
import pymongo
import pandas as pd

client = pymongo.MongoClient('localhost', 27017)
db = client.TweetAnalysis
db = pymongo.MongoClient().Tweetsdb
def map_gen():
    
  # get geo data only from rows with non-empty values
  #locations = pandas.read_csv('./tweets.csv', usecols=[3]).dropna()
  query={}
  projection={"geo":1}
  cursor = db.Tweets.find(query,projection)
  geos = []
  for a in cursor:
    if a['geo'] != None:
      geos.append(a['geo']['coordinates'])


  # initialize and create map
  tweet_map = folium.Map(location=[52.8, -2], tiles='Mapbox Bright', zoom_start=2)

  # add markers
  for geo in geos:
    #tweet_map.CircleMarker(geo, radius=250)
    folium.CircleMarker(geo,
                      radius=500,
                      color='#3186cc',
                      fill_color='#3186cc', ).add_to(tweet_map)
  tweet_map.save('map_v2.html')
