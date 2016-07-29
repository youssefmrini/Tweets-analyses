import tweepy
import sys
import json
import urllib
import urllib2
import pymongo
import yaml
from tweepy import OAuthHandler, Stream, API
from tweepy.streaming import StreamListener
from PyQt4 import QtCore, QtGui
from bestTweet import *
from findhash import *
from map_final import *
from map_parmot_v3 import *
from word_freq_final import *
from stats import *
from nltk import FreqDist
import pandas as pd
import webbrowser
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from map_parmot_v4 import *
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)
"""
consumer_key="we4UpK0qb6RpyzIy9ObxY7jcU"
consumer_secret="cvqhQEXbzBCa8yh2373adMwZyD8BKAbA2ppiBt4AU7r8wuYBac"

access_token="543832492-XF743YzMO2OrDQsSSpVjPQYdCvsG4DtdDbrU3I0B"
access_token_secret="VOLSLSdPgCgDYQEe4vCaR2Iozdd96t49ZdTf2b0ZNXePn"
"""
consumer_key="zWD24qbfbG1jz6DFBPBexdNqz"
consumer_secret="3btxJx6B5zvpVqToQXwUT5PZ0708y4ogvvSJlH0WJcpOetS1iA"

access_token="125108625-a3i1NFxqTPZF2CJ5zK9v1zvdjWri2UCNAnl6P2rj"
access_token_secret="22uVQZGGMpXorrJJT76gAo6DGHhGx2Es7oZ26WUFMZeZ4"

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
        print data['text']
        if (data['user']['lang'] == 'en' or data['user']['lang'] == 'fr'):
                
            sent = getsentiment(data['text'])
            data['sentimentRating'] = sent
        else :
            data['sentimentRating'] = 0.0
        data['sentimentRating'] = sent
        self.db.Tweets.insert(data)
        ui.OutPutText_stream.insertPlainText(data['text']+'\n')
    def on_data(self, tweet):
        print tweet['text']
    def on_error(self, status):
        print >> sys.stderr, 'Error: ', status
        return True

    def on_timeout(self):
        print >> sys.stderr, 'Stream timeout'
        return True

def start_stream_tweet(val):
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = API(auth)
    listen = Stream(auth, CustomListener(api))        
    if val == 'Null':
        listen.filter(locations=[-180,-90,180,90])
        #listen.filter(track = 'the')

    else :
        listen.filter(track = [val])


class Ui_MainWindow(object):
    value_radio_stream = 0
    radio_stream_anal=0
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(801, 594)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("micon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setWindowOpacity(1000000.0)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(-1, -1, 805, 561))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.StreamTweet = QtGui.QTabWidget(self.gridLayoutWidget)
        self.StreamTweet.setEnabled(True)
        self.StreamTweet.setMouseTracking(False)
        self.StreamTweet.setFocusPolicy(QtCore.Qt.NoFocus)
        self.StreamTweet.setObjectName(_fromUtf8("StreamTweet"))
        self.Stream = QtGui.QWidget()
        self.Stream.setObjectName(_fromUtf8("Stream"))
        self.OutPutText_stream = QtGui.QTextEdit(self.Stream)
        self.OutPutText_stream.setGeometry(QtCore.QRect(20, 170, 751, 340))
        self.OutPutText_stream.setReadOnly(True)
        self.OutPutText_stream.setObjectName(_fromUtf8("OutPutText_stream"))
        self.button_StartStream = QtGui.QPushButton(self.Stream)
        self.button_StartStream.setGeometry(QtCore.QRect(400, 120, 181, 23))
        self.button_StartStream.setObjectName(_fromUtf8("button_StartStream"))
        self.label = QtGui.QLabel(self.Stream)
        self.label.setGeometry(QtCore.QRect(21, 101, 81, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.line_stream = QtGui.QLineEdit(self.Stream)
        self.line_stream.setEnabled(True)
        self.line_stream.setGeometry(QtCore.QRect(21, 120, 361, 20))
        self.line_stream.setObjectName(_fromUtf8("line_stream"))
        self.groupBox = QtGui.QGroupBox(self.Stream)
        self.groupBox.setGeometry(QtCore.QRect(20, 10, 751, 81))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.WorldWide = QtGui.QRadioButton(self.groupBox)
        self.WorldWide.setGeometry(QtCore.QRect(10, 30, 372, 20))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("earth-skull.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.WorldWide.setIcon(icon1)
        self.WorldWide.setChecked(False)
        self.WorldWide.setObjectName(_fromUtf8("WorldWide"))
        self.wordtrack = QtGui.QRadioButton(self.groupBox)
        self.wordtrack.setGeometry(QtCore.QRect(360, 30, 749, 20))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8("7df3h38zabcvjylnyfe3.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.wordtrack.setIcon(icon2)
        self.wordtrack.setObjectName(_fromUtf8("wordtrack"))
        self.button_StopStream = QtGui.QPushButton(self.Stream)
        self.button_StopStream.setGeometry(QtCore.QRect(604, 120, 171, 23))
        self.button_StopStream.setObjectName(_fromUtf8("button_StopStream"))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8("illu_animez-une-communaute-twitter.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.StreamTweet.addTab(self.Stream, icon3, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.Tewtbteweet = QtGui.QTextEdit(self.tab_2)
        self.Tewtbteweet.setGeometry(QtCore.QRect(20, 110, 381, 181))
        self.Tewtbteweet.setReadOnly(True)
        self.Tewtbteweet.setObjectName(_fromUtf8("Tewtbteweet"))
        self.texthtag = QtGui.QTextEdit(self.tab_2)
        self.texthtag.setGeometry(QtCore.QRect(420, 110, 341, 181))
        self.texthtag.setReadOnly(True)
        self.texthtag.setObjectName(_fromUtf8("texthtag"))
        self.label_3 = QtGui.QLabel(self.tab_2)
        self.label_3.setGeometry(QtCore.QRect(150, 90, 121, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.textwtweet = QtGui.QTextEdit(self.tab_2)
        self.textwtweet.setGeometry(QtCore.QRect(20, 330, 381, 181))
        self.textwtweet.setReadOnly(True)
        self.textwtweet.setObjectName(_fromUtf8("textwtweet"))
        self.label_4 = QtGui.QLabel(self.tab_2)
        self.label_4.setGeometry(QtCore.QRect(150, 300, 121, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(self.tab_2)
        self.label_5.setGeometry(QtCore.QRect(540, 90, 46, 13))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.verticalLayoutWidget = QtGui.QWidget(self.tab_2)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(479, 329, 231, 181))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.Button_map = QtGui.QPushButton(self.verticalLayoutWidget)
        self.Button_map.setObjectName(_fromUtf8("Button_map"))
        self.verticalLayout.addWidget(self.Button_map)
        self.verticalLayout.addWidget(self.Button_map)
        self.generate_map_sentiment = QtGui.QPushButton(self.verticalLayoutWidget)
        self.generate_map_sentiment.setObjectName(_fromUtf8("generate_map_sentiment"))
        self.verticalLayout.addWidget(self.generate_map_sentiment)
        
        self.Button_freq_word = QtGui.QPushButton(self.verticalLayoutWidget)
        self.Button_freq_word.setObjectName(_fromUtf8("Button_freq_word"))
        self.verticalLayout.addWidget(self.Button_freq_word)
        self.Button_sentiment = QtGui.QPushButton(self.verticalLayoutWidget)
        self.Button_sentiment.setObjectName(_fromUtf8("Button_sentiment"))
        self.verticalLayout.addWidget(self.Button_sentiment)

        

        self.groupBox_3 = QtGui.QGroupBox(self.tab_2)
        self.groupBox_3.setGeometry(QtCore.QRect(20, 55, 751, 31))
        self.groupBox_3.setTitle(_fromUtf8(""))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        


        
        
        #self.layoutWidget = QtGui.QWidget(self.tab_2)
        #self.layoutWidget.setGeometry(QtCore.QRect(20, 50, 750, 41))
        #self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        #self.horizontalLayout_3 = QtGui.QHBoxLayout(self.layoutWidget)
        #self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        #        self.label_2 = QtGui.QLabel(self.layoutWidget)
        self.label_2 = QtGui.QLabel(self.tab_2)
        self.label_2.setGeometry(QtCore.QRect(17, 51, 84, 39))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.line_analyse = QtGui.QLineEdit(self.tab_2)
        self.line_analyse.setEnabled(True)
        self.line_analyse.setGeometry(QtCore.QRect(115, 61, 381, 20))
        self.line_analyse.setObjectName(_fromUtf8("line_analyse"))
        self.button_StartAnalysis = QtGui.QPushButton(self.tab_2)
        self.button_StartAnalysis.setGeometry(QtCore.QRect(508, 59, 251, 23))
        self.button_StartAnalysis.setObjectName(_fromUtf8("button_StartAnalysis"))

        self.groupBox_2 = QtGui.QGroupBox(self.tab_2)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 0, 751, 51))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.WordTweet = QtGui.QRadioButton(self.groupBox_2)
        self.WordTweet.setEnabled(True)
        self.WordTweet.setGeometry(QtCore.QRect(70, 20, 371, 20))
        self.WordTweet.setIcon(icon2)
        self.WordTweet.setObjectName(_fromUtf8("WordTweet"))
        self.AllTweets = QtGui.QRadioButton(self.groupBox_2)
        self.AllTweets.setGeometry(QtCore.QRect(430, 20, 749, 20))
        self.AllTweets.setIcon(icon1)
        self.AllTweets.setChecked(False)
        self.AllTweets.setObjectName(_fromUtf8("AllTweets"))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8("Twitter-statistiques-700x325.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.StreamTweet.addTab(self.tab_2, icon4, _fromUtf8(""))
        self.gridLayout.addWidget(self.StreamTweet, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 799, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuAbout = QtGui.QMenu(self.menubar)
        self.menuAbout.setObjectName(_fromUtf8("menuAbout"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        self.StreamTweet.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MongoTweet", None))
        self.button_StartStream.setText(_translate("MainWindow", "Start Streaming", None))
        self.label.setText(_translate("MainWindow", "Enter Track word", None))
        self.groupBox.setTitle(_translate("MainWindow", "Search Type", None))
        self.WorldWide.setText(_translate("MainWindow", "World Wide Track", None))
        self.wordtrack.setText(_translate("MainWindow", "Track By word", None))

        self.button_StopStream.setText(_translate("MainWindow", "Stop Streaming", None))
        self.StreamTweet.setTabText(self.StreamTweet.indexOf(self.Stream), _translate("MainWindow", "Stream Tweets", None))
        self.label_3.setText(_translate("MainWindow", "Best Tweets", None))
        self.label_4.setText(_translate("MainWindow", "Worst Tweets", None))
        self.label_5.setText(_translate("MainWindow", "Hashtags", None))
        self.Button_map.setText(_translate("MainWindow", "Generate Map", None))
        self.generate_map_sentiment.setText(_translate("MainWindow", "Generate Map With Sentiments", None))

        self.Button_freq_word.setText(_translate("MainWindow", "Frequent Words", None))
        self.Button_sentiment.setText(_translate("MainWindow", "Sentiments Statistics", None))
        self.label_2.setText(_translate("MainWindow", "  Tape your word ", None))
        self.button_StartAnalysis.setText(_translate("MainWindow", "Start Analysis", None))
        self.groupBox_2.setTitle(_translate("MainWindow", "Search Type", None))
        self.WordTweet.setText(_translate("MainWindow", "Choose Word", None))
        self.AllTweets.setText(_translate("MainWindow", "All Tweets", None))
        self.StreamTweet.setTabText(self.StreamTweet.indexOf(self.tab_2), _translate("MainWindow", "Tweets Analysis", None))
        self.menuAbout.setTitle(_translate("MainWindow", "about", None))

        QtCore.QObject.connect(self.WorldWide,QtCore.SIGNAL("clicked()"),self.radio_value)
        QtCore.QObject.connect(self.wordtrack,QtCore.SIGNAL("clicked()"),self.radio_value)
        QtCore.QObject.connect(self.button_StartStream,QtCore.SIGNAL("clicked()"),self.StartStream)

        QtCore.QObject.connect(self.WordTweet,QtCore.SIGNAL("clicked()"),self.radio_stream_value)
        QtCore.QObject.connect(self.AllTweets,QtCore.SIGNAL("clicked()"),self.radio_stream_value)
        QtCore.QObject.connect(self.button_StartAnalysis,QtCore.SIGNAL("clicked()"),self.StartAnalysis)

        QtCore.QObject.connect(self.Button_map,QtCore.SIGNAL("clicked()"),self.StartMap)
        QtCore.QObject.connect(self.Button_freq_word,QtCore.SIGNAL("clicked()"),self.Startfreq_word)
        QtCore.QObject.connect(self.Button_sentiment,QtCore.SIGNAL("clicked()"),self.Startsentiment)
        QtCore.QObject.connect(self.generate_map_sentiment,QtCore.SIGNAL("clicked()"),self.gene_map_sent)
        QtCore.QObject.connect(self.button_StopStream,QtCore.SIGNAL("clicked()"),self.stopfunc)

        
    def stopfunc(self):
        return 0

    def radio_value(self):
        if self.WorldWide.isChecked():
            value_radio_stream = 1
            self.line_stream.setEnabled(False)

        elif self.wordtrack.isChecked():
            value_radio_stream = 2
            self.line_stream.setEnabled(True)
        else :
            value_radio_stream = 3
        
        return value_radio_stream
    def StartStream(self):
        self.OutPutText_stream.insertPlainText('start  \n\n')
        try: 
            if self.radio_value() == 1:
                self.db = pymongo.MongoClient().Tweetsdb
                x=self.db.Tweets.find()
                self.OutPutText_stream.setText(" ")
                
                for i in x:
                    #print(i['text'])
                    
                    

                   # time.sleep(0.01)
                    #self.OutPutText_stream.append(i+'\n')
                    #self.OutPutText_stream.insertPlainText('a'+'\n')
                    self.OutPutText_stream.append(i['text']+'\n')
                    
                    
                   
                                
                
                
            elif self.radio_value() == 2 and self.line_stream.text() == '':
                self.showdialog_word_empty()
                
            elif self.radio_value() == 2:
                find=self.line_stream.text()
                connect(find)
                self.db = pymongo.MongoClient().Tweetsdb
                x=self.db.Tweetfind.find()
                self.OutPutText_stream.setText("")
               
                
                for i in x:
                    #print(i['text'])
                    

                
                    
                    #self.OutPutText_stream.insertPlainText('a'+'\n')
                    self.OutPutText_stream.append(i['text']+'\n')
                    
                    
                

            else:
                self.showdialog()
        except:
            pass
            
    def radio_stream_value(self):
        if self.WordTweet.isChecked():
            radio_stream_anal = 1
            self.line_analyse.setEnabled(True)

        elif self.AllTweets.isChecked():
            radio_stream_anal = 2
            self.line_analyse.setEnabled(False)
        else :
            radio_stream_anal = 3

        return radio_stream_anal
    def StartAnalysis(self):
        contpos = 0
        contnig = 0
        print self.line_stream.text()
        if self.radio_stream_value() == 1 and self.line_analyse.text() == '':
                self.showdialog_word_empty()
                return 0
        
        elif self.radio_stream_value() == 1:
            word_analyse = self.line_analyse.text()
            dic = findhash_word(word_analyse)
        elif self.radio_stream_value() == 2:
            word_analyse = '0661168090'
            dic = findhash()
            print type(dic)
        else :
            self.showdialog()
            return 0
        cursorBT = bestTweet(word_analyse)
        self.textwtweet.setText(" ")
        self.Tewtbteweet.setText(" ")
        for tweet_zwin in cursorBT :
            if tweet_zwin['sentimentRating'] >= 0.0 and contpos < 3:
                contpos = contpos + 1
                self.Tewtbteweet.append(tweet_zwin['text']+'\n')
            elif tweet_zwin['sentimentRating'] <= 0.0 and contnig < 3:
                contnig = contnig + 1                
                self.textwtweet.append(tweet_zwin['text']+'\n')
        #____________________________________________________________________
        self.texthtag.setText(str(dic))

    def StartMap(self):
        if self.radio_stream_value() == 1:
            word_analyse = self.line_analyse.text()
            geomap(word_analyse)
            webbrowser.open("map_v3.html")
        elif self.radio_stream_value() == 2:
            map_gen()
            webbrowser.open("map_v2.html")
            

    def Startfreq_word(self):
        if self.radio_stream_value() == 1:
            word_analyse = self.line_analyse.text()
            freq_dist = freqgen_word(word_analyse)
            aa = nltk.probability.FreqDist(freq_dist)
            print aa.plot(25)
        elif self.radio_stream_value() == 2:
            freq_dist = freqgen()
            aa = nltk.probability.FreqDist(freq_dist)
            print aa.plot(25)
            
    def Startsentiment(self):
        if self.radio_stream_value() == 1:
            word_analyse = self.line_analyse.text()
            statistics_word(word_analyse)
        elif self.radio_stream_value() == 2:
            statistics_simple()
    def showdialog_word_empty(self):
        msg1 = QMessageBox()
        msg1.setIcon(QMessageBox.Information)
        msg1.setText(" feel the blank with a word")
        msg1.setWindowTitle("HODOOOOOR")
        msg1.setStandardButtons(QMessageBox.Ok )
        msg1.buttonClicked.connect(self.msg1btn)
        retval1 = msg1.exec_()
        print "value of pressed message box button:", retval1
	
    def msg1btn(self,i):
       print "Button pressed is:",i.text()

    def showdialog(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("damn you need to choose an option man !!!!")
        msg.setWindowTitle("Your computer is about to explode")
        msg.setStandardButtons(QMessageBox.Retry  )
        msg.buttonClicked.connect(self.msgbtn)
        retval = msg.exec_()
        print "value of pressed message box button:", retval

    def msgbtn(self,i):
       print "Button pressed is:",i.text()
    def gene_map_sent(self):
        if self.radio_stream_value() == 1:
            word_analyse = self.line_analyse.text()
            geomap_col_mot(word_analyse)
            webbrowser.open("map_col_mot.html")
        elif self.radio_stream_value() == 2:
            geomap_col()
            webbrowser.open("map_col_all.html")

if __name__ == "__main__":
    import sys

    
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

