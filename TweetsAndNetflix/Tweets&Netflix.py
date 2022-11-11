# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 09:54:50 2022

@author: chase
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import snscrape.modules.twitter as sntwitter
import time
import re
from textblob import TextBlob
import statsmodels.formula.api as sm
from stargazer.stargazer import Stargazer
from IPython.core.display import HTML
import webbrowser
import matplotlib as mpl



os.chdir(r'C:\Users\chase\GDrive\GD_Work\SoDA496\TweetsAndNetflix')

#Import and prepare Netflix NASDAQ dataset
df_Net = pd.read_csv('Netflix_NASDAQ.csv')

df_Net.rename(columns = {'Close/Last':'close'}, inplace = True) #Rename Close/Last column

df_Net['close'] = [float(x[1:]) for x in df_Net['close']] #Remove dollar sign
df_Net['Date'] = [datetime.strptime(x, '%m/%d/%Y').date() for x in df_Net['Date']] #Convert Date column to date format

plt.plot(df_Net['Date'], df_Net['close']) #Plot a time series graph


#Scrape for Tweets using snscrape
attributes_container = []

#https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query
since = df_Net['Date']
until = df_Net['Date'] + timedelta(days=1)
for j in range(len(df_Net)):
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper('Netflix lang:en since:' + str(since[j]) + ' until:' + str(until[j]) +  ' -is:retweet').get_items()):
        if i>50:
            break
        attributes_container.append([tweet.user.username, tweet.date, tweet.likeCount, tweet.sourceLabel, tweet.rawContent])
    print('Scraping ' + str(j) + ' out of ' + str(len(df_Net)))
    time.sleep(2)
    
# Creating a dataframe to load the list
tweets_df = pd.DataFrame(attributes_container, columns=["User", "Date Created", "Number of Likes", "Source of Tweet", "Tweet"])
#tweets_df.to_csv(r'Netflix_tweets.csv', index = False)

#Import dataframe if Tweets have already been scraped
tweets_df = pd.read_csv('Netflix_tweets.csv')

#Clean tweets and run sentiment analysis using TextBlob
tweet_sent = []
for tweet in tweets_df['Tweet']:

    clean_tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
    
    # create TextBlob object of passed tweet text
    analysis = TextBlob(clean_tweet)
    # set sentiment
    if analysis.sentiment.polarity > 0:
        tweet_sent.append(1)
    elif analysis.sentiment.polarity == 0:
        tweet_sent.append(0)
    else:
        tweet_sent.append(-1)
        
#Get number of positive, negative, and neutral tweets
ptweets = len([tweet for tweet in tweet_sent if tweet == 1])
ntweets = len([tweet for tweet in tweet_sent if tweet == 0])
neut_tweets = len(tweet_sent) - (ptweets + ntweets)


mpl.rcParams['axes.spines.right'] = False
mpl.rcParams['axes.spines.top'] = False


colors = {'Positive':'blue', 'Negative':'red', 'Neutral':'green'}         
labels = list(colors.keys())
handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
plt.bar([1,2,3], [ptweets, ntweets, neut_tweets], color = ['blue', 'red', 'green'])
plt.title('Polarity of Netflix Tweets')
plt.ylabel('Number of Tweets')
plt.legend(handles, labels)
plt.xticks([])

plt.show()

#Add sentiment to dataframe and convert Date Created column to date format
tweets_df['sent'] = tweet_sent
tweets_df['Date'] = [datetime.strptime(x[0:10], '%Y-%m-%d').date() for x in tweets_df['Date Created']]

#Aggregate Tweet sentiment by day
df_agg = tweets_df.groupby('Date').sum()

#Merge Tweet data with Netflix performance data using the day
df = df_Net.merge(df_agg, left_on = 'Date', right_on ='Date')

#Plot a time series graph looking at both sentiment and Netflix's stock performance
colors = {'Stock Price (10s of USD)':'blue', 'Daily Sentiment':'orange'}         
labels = list(colors.keys())
handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
plt.plot(df['Date'], df['close']/10)
plt.plot(df['Date'], df['sent'])
plt.legend(handles, labels)
plt.title('Netflix Stock Price and Twitter Sentiment Overtime')
plt.savefig('NetflixPlot.png')
plt.show()

#Scatterplot of the relationship between Netflix sentiment and stock performance
plt.scatter(df['sent'], df['close']/10)
plt.show()

#Simple linear regression of Netflix sentiment and stock performance
model = sm.ols(formula = 'close ~ sent', data = df).fit()

#Create, save, and open regression table 
output = Stargazer([model])
table = HTML(output.render_html())

with open("table.html", "w") as file:
    file.write(table.data)
    
webbrowser.open('table.html')



