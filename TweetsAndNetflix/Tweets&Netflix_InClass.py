# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 14:52:12 2022

@author: chase
"""

import os
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import snscrape.modules.twitter as sntwitter
import time
from textblob import TextBlob
import regex as re
import matplotlib as mpl
import statsmodels.formula.api as sm
from stargazer.stargazer import Stargazer
from IPython.core.display import HTML
import webbrowser


os.chdir(r'C:\Users\chase\GDrive\GD_Work\SoDA496\TweetsAndNetflix')

df_Net = pd.read_csv('Netflix_NASDAQ.csv')

df_Net.rename(columns = {'Close/Last':'close'}, inplace = True)

df_Net['close'] = [float(x[1:]) for x in df_Net['close']]

df_Net['Date'] = [datetime.strptime(x, '%m/%d/%Y').date() for x in df_Net['Date']]
type(df_Net['Date'][1])

plt.plot(df_Net['Date'], df_Net['close'])
plt.show()

since = df_Net['Date']
until = df_Net['Date'] + timedelta(days = 1)

attributes_container = []

for j in range(len(df_Net)):
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper('Netflix lang:en since:' + 
                                                             str(since[j]) + 'until:' + str(until[j]) + '-is:retweet').get_items()):
        if i>50:
            break
        attributes_container.append([tweet.date,tweet.rawContent])
    print('Scraping ' + str(j) + ' out of ' + str(len(df_Net)))
    time.sleep(2)
 
       
#tweets_df = pd.DataFrame(attributes_container, columns=['Date Created', 'Tweet'])

tweets_df = pd.read_csv('Netflix_tweets.csv')

tweet_sent = []
for tweet in tweets_df['Tweet']:
    clean_tweet = ' '.join(re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z /t])|(\w+:\/\/\S+)', " ", tweet).split())
    
    analysis = TextBlob(clean_tweet)
    
    if analysis.sentiment.polarity > 0:
        tweet_sent.append(1)
    elif analysis.sentiment.polarity == 0:
        tweet_sent.append(0)
    else:
        tweet_sent.append(-1)
    
ptweets = len([tweet for tweet in tweet_sent if tweet == 1])
ntweets = len([tweet for tweet in tweet_sent if tweet == -1])
neut_tweets = len(tweet_sent) - (ptweets + ntweets)


mpl.rcParams['axes.spines.right'] =False
mpl.rcParams['axes.spines.top'] =False


colors = {'Positive': 'blue', 'Negative':'red', 'Neutral':'green'}
labels = list(colors.keys())
handles = [plt.Rectangle((0,0),1,1,color=colors[label]) for label in labels]
plt.bar([1,2,3], [ptweets, ntweets, neut_tweets], color = ['blue', 'red', 'green'])
plt.title('Polarity of Netflix Tweets')
plt.ylabel('Number of Tweets')
plt.legend(handles, labels)
plt.xticks([])
plt.savefig('NetflixSentiment.png')
plt.show()

tweets_df['sent'] = tweet_sent

tweets_df['Date'] = [datetime.strptime(x[0:10], '%Y-%m-%d').date() for x in tweets_df['Date Created']]

df_agg = tweets_df.groupby('Date Created')['sent'].sum()

df = df_Net.merge(df_agg, left_on = 'Date', right_on = 'Date Created')

plt.scatter(df['sent'], df['close'])
plt.show()

plt.plot(df['Date'], df['close']/10)
plt.plot(df['Date'], df['sent'])
plt.show

model = sm.ols(formula = 'close ~ sent', data =df).fit()

#Create, save, and open regression table 
output = Stargazer([model])
table = HTML(output.render_html())

with open("table.html", "w") as file:
    file.write(table.data)
    
webbrowser.open('table.html')


















