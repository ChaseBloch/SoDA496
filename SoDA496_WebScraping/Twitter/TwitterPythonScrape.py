##https://www.freecodecamp.org/news/python-web-scraping-tutorial/#:~:text=Tweepy%20is%20a%20Python%20library,of%20the%20Twitter%20API's%20capabilities.

import tweepy
import pandas as pd
import snscrape.modules.twitter as sntwitter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import nltk 
from PIL import Image

os.chdir(r'C:\Users\chase\GDrive\GD_Work\SoDA496\SoDA496_WebScraping\Twitter')


API_key = 'F4mASP12B1oaWjrnjXGI2Xz4K'
API_secret = '0NYpbio5ELLIDHMKUG1SheYZrMQU5vO8QfcoiscMZlRWMO9PTn'
Access_token = '1057441879523057669-yispuKmbRB4IA7Dc8IyOH1ZwzCb9Lb'
Access_secret = 'b2g9KikltoYAwQJht0jdiFWb6wvnrHaEQ8RjPa7d6Zzk3'
bearer_token = ('AAAAAAAAAAAAAAAAAAAAAHRCigEAAAAACLKPyAhQWf3rNbi1mS6kqeW8'
                'gbI%3D5G7YpKuTZoWJIWZIQu942kPq2YhUdhuEPgw8x11jtzIX248VeX')

# Pass in our twitter API authentication key.
auth = tweepy.OAuth1UserHandler(
    API_key, API_secret,
    Access_token, Access_secret
)

# Instantiate the tweepy API.
api = tweepy.API(auth, wait_on_rate_limit=True)

search_query = "Covid-19"
no_of_tweets = 100

try:
    # The number of tweets we want to retrieved from the search.
    tweets = api.search_tweets(q=search_query, count=no_of_tweets, lang = 'en')
    
    # Pulling Some attributes from the tweet.
    attributes_container = [
        [tweet.user.name, tweet.created_at, 
         tweet.favorite_count, tweet.source, tweet.text
         ] for tweet in tweets]

    # Creation of column list to rename the columns in the dataframe.
    columns = [
        "User", "Date Created", 
        "Number of Likes", "Source of Tweet", "Tweet"
        ]
    
    # Create the dataframe.
    tweets_df = pd.DataFrame(attributes_container, columns=columns)
except BaseException as e:
    print('Status Failed On,',str(e))
    
    
### Using the paginator method
client = tweepy.Client(bearer_token=bearer_token)

query = 'Covid-19 -is:retweet lang:en'
tweets = tweepy.Paginator(
    client.search_recent_tweets, query=query, 
    tweet_fields=['author_id','context_annotations', 'created_at'], 
    max_results=100
    ).flatten(limit=500)

tweets_df2 = pd.DataFrame(tweets)


### Using SNScrape

# No Stop Words
#%%
# Creating list to append tweet data to.
attributes_container = []

# Using TwitterSearchScraper to scrape data and append tweets to list.
for i,tweet in enumerate(sntwitter.TwitterSearchScraper(
        'Covid-19 lang:en since:2021-07-05 until:2021-07-06'
        ).get_items()):
    if i>500:
        break
    attributes_container.append(
        [tweet.user.username, tweet.date, 
         tweet.likeCount, tweet.sourceLabel, 
         tweet.rawContent]
        )
    
# Creating a dataframe to load the list.
tweets_df = pd.DataFrame(
    attributes_container, 
    columns=[
        "User", "Date Created", "Number of Likes", "Source of Tweet", "Tweet"
        ]
    )
del attributes_container

vectorizer = TfidfVectorizer(
    stop_words='english', ngram_range = (1,1), max_df = .9, min_df = .01
    )
X = vectorizer.fit_transform(tweets_df['Tweet'])
feature_names = vectorizer.get_feature_names_out()

dense = X.todense()
denselist = dense.tolist()
df = pd.DataFrame(denselist, columns=feature_names)

df_avg = df.mean(axis=0)

# change the value to black
def black_color_func(
        word, font_size, position,orientation,random_state=None, **kwargs
        ):
    return("hsl(0,100%, 1%)")
# set the wordcloud background color to white
# set max_words to 1000
# set width and height to higher quality, 3000 x 2000
wordcloud = WordCloud(
    background_color="white", 
    width=3000, height=2000, max_words=500
    ).generate_from_frequencies(df_avg)
# set the word color to black
wordcloud.recolor(color_func = black_color_func)
# set the figsize
plt.figure(figsize=[15,10])
# plot the wordcloud
plt.imshow(wordcloud, interpolation="bilinear")
# remove plot axes
plt.xticks([])
plt.yticks([])
plt.title('Covid-19', fontdict={'fontsize': 50})
# save the image
plt.savefig('Covid-19.png')
#%%

# Covid19
#%%
# Creating list to append tweet data to.
attributes_container = []

# Using TwitterSearchScraper to scrape data and append tweets to list.
for i,tweet in enumerate(sntwitter.TwitterSearchScraper(
        'Covid19 lang:en since:2021-07-05 until:2021-07-06'
        ).get_items()):
    if i>500:
        break
    attributes_container.append(
        [tweet.user.username, tweet.date, 
         tweet.likeCount, tweet.sourceLabel, tweet.rawContent]
        )
    
# Creating a dataframe to load the list.
tweets_df = pd.DataFrame(
    attributes_container, 
    columns=[
        "User", "Date Created", 
        "Number of Likes", "Source of Tweet", "Tweet"
        ]
    )
del attributes_container

vectorizer = TfidfVectorizer(
    stop_words='english', ngram_range = (1,1), max_df = .9, min_df = .01
    )

X = vectorizer.fit_transform(tweets_df['Tweet'])
feature_names = vectorizer.get_feature_names_out()

dense = X.todense()
denselist = dense.tolist()
df = pd.DataFrame(denselist, columns=feature_names)
df = df.drop('https', axis = 1)
df_avg = df.mean(axis=0)

# change the value to black
def black_color_func(
        word, font_size, position,orientation,random_state=None, **kwargs
        ):
    return("hsl(0,100%, 1%)")
# set the wordcloud background color to white
# set max_words to 1000
# set width and height to higher quality, 3000 x 2000
wordcloud = WordCloud(
    background_color="white", 
    width=3000, height=2000, max_words=500
    ).generate_from_frequencies(df_avg)
# set the word color to black
wordcloud.recolor(color_func = black_color_func)
# set the figsize
plt.figure(figsize=[15,10])
# plot the wordcloud
plt.imshow(wordcloud, interpolation="bilinear")
# remove plot axes
plt.xticks([])
plt.yticks([])
plt.title('Covid19', fontdict={'fontsize': 50})
# save the image
plt.savefig('Covid19.png')
#%%

# Coronavirus
#%%
# Creating list to append tweet data to.
attributes_container = []

# Using TwitterSearchScraper to scrape data and append tweets to list.
for i,tweet in enumerate(sntwitter.TwitterSearchScraper(
        'coronavirus lang:en since:2021-07-05 until:2021-07-06'
        ).get_items()):
    if i>500:
        break
    attributes_container.append(
        [tweet.user.username, tweet.date, 
         tweet.likeCount, tweet.sourceLabel, tweet.rawContent]
        )
    
# Creating a dataframe to load the list.
tweets_df = pd.DataFrame(
    attributes_container, 
    columns=[
        "User", "Date Created", "Number of Likes", "Source of Tweet", "Tweet"
        ]
    )
del attributes_container

vectorizer = TfidfVectorizer(
    stop_words='english', 
    ngram_range = (1,1), max_df = .9, min_df = .01
    )

X = vectorizer.fit_transform(tweets_df['Tweet'])
feature_names = vectorizer.get_feature_names_out()

dense = X.todense()
denselist = dense.tolist()
df = pd.DataFrame(denselist, columns=feature_names)
df = df.drop('https', axis = 1)

df_avg = df.mean(axis=0)

# change the value to black
def black_color_func(
        word, font_size, position,orientation,random_state=None, **kwargs
        ):
    return("hsl(0,100%, 1%)")
# set the wordcloud background color to white
# set max_words to 1000
# set width and height to higher quality, 3000 x 2000
wordcloud = WordCloud(
    background_color="white", 
    width=3000, height=2000, max_words=500
    ).generate_from_frequencies(df_avg)
# set the word color to black
wordcloud.recolor(color_func = black_color_func)
# set the figsize
plt.figure(figsize=[15,10])
# plot the wordcloud
plt.imshow(wordcloud, interpolation="bilinear")
# remove plot axes
plt.xticks([])
plt.yticks([])
plt.title('Coronavirus', fontdict={'fontsize': 50})
# save the image
plt.savefig('Coronavirus.png')
#%%


# Stop Words
#%%
attributes_container = []

# Using TwitterSearchScraper to scrape data and append tweets to list.
for i,tweet in enumerate(sntwitter.TwitterSearchScraper(
        'Covid-19 lang:en since:2021-07-05 until:2021-07-06'
        ).get_items()):
    if i>500:
        break
    attributes_container.append(
        [tweet.user.username, tweet.date, 
         tweet.likeCount, tweet.sourceLabel, tweet.rawContent
         ])
    
# Creating a dataframe to load the list.
tweets_df = pd.DataFrame(
    attributes_container, 
    columns=[
        "User", "Date Created", 
        "Number of Likes", "Source of Tweet", "Tweet"
        ]
    )
del attributes_container

vectorizer = TfidfVectorizer(ngram_range = (1,1), max_df = .9, min_df = .01)

X = vectorizer.fit_transform(tweets_df['Tweet'])
feature_names = vectorizer.get_feature_names_out()

dense = X.todense()
denselist = dense.tolist()
df = pd.DataFrame(denselist, columns=feature_names)
df = df.drop('https', axis = 1)

df_avg = df.mean(axis=0)

# change the value to black
def black_color_func(
        word, font_size, position,orientation,random_state=None, **kwargs
        ):
    return("hsl(0,100%, 1%)")
# set the wordcloud background color to white
# set max_words to 1000
# set width and height to higher quality, 3000 x 2000
wordcloud = WordCloud(
    background_color="white", 
    width=3000, height=2000, max_words=500
    ).generate_from_frequencies(df_avg)
# set the word color to black
wordcloud.recolor(color_func = black_color_func)
# set the figsize
plt.figure(figsize=[15,10])
# plot the wordcloud
plt.imshow(wordcloud, interpolation="bilinear")
# remove plot axes
plt.xticks([])
plt.yticks([])
plt.title('Covid-19 With Stopwords', fontdict={'fontsize': 50})
# save the image
plt.savefig('Covid-19_stopwords.png')
#%%

# Covid-19 Stemmed
#%%
# Creating list to append tweet data to.
attributes_container = []

# Using TwitterSearchScraper to scrape data and append tweets to list.
for i,tweet in enumerate(sntwitter.TwitterSearchScraper(
        'Covid19 lang:en since:2021-07-05 until:2021-07-06'
        ).get_items()):
    if i>500:
        break
    attributes_container.append(
        [tweet.user.username, tweet.date,
         tweet.likeCount, tweet.sourceLabel, tweet.rawContent]
        )
    
# Creating a dataframe to load the list.
tweets_df = pd.DataFrame(
    attributes_container, 
    columns=[
        "User", "Date Created", 
        "Number of Likes", "Source of Tweet", "Tweet"
        ]
    )
del attributes_container
 
stemmer = nltk.stem.PorterStemmer()
class StemmedTfidfVectorizer(TfidfVectorizer):
    def build_analyzer(self):
        analyzer = super(StemmedTfidfVectorizer, self).build_analyzer()
        return lambda doc: ([stemmer.stem(w) for w in analyzer(doc)])

vectorizer = StemmedTfidfVectorizer(
    stop_words='english', ngram_range = (1,1), max_df = .9, min_df = .01
    )

X = vectorizer.fit_transform(tweets_df['Tweet'])
feature_names = vectorizer.get_feature_names_out()

dense = X.todense()
denselist = dense.tolist()
df = pd.DataFrame(denselist, columns=feature_names)
df = df.drop('http', axis = 1)

df_avg = df.mean(axis=0)

# change the value to black
def black_color_func(
        word, font_size, position,orientation,random_state=None, **kwargs
        ):
    return("hsl(0,100%, 1%)")
# set the wordcloud background color to white
# set max_words to 1000
# set width and height to higher quality, 3000 x 2000
wordcloud = WordCloud(
    background_color="white", 
    width=3000, height=2000, max_words=500
    ).generate_from_frequencies(df_avg)
# set the word color to black
wordcloud.recolor(color_func = black_color_func)
# set the figsize
plt.figure(figsize=[15,10])
# plot the wordcloud
plt.imshow(wordcloud, interpolation="bilinear")
# remove plot axes
plt.xticks([])
plt.yticks([])
plt.title('Covid-19 Stemmed', fontdict={'fontsize': 50})
# save the image
plt.savefig('Covid-19_stemmed.png')
#%%

# Covid-19 Bigrams
#%%
# Creating list to append tweet data to
attributes_container = []

# Using TwitterSearchScraper to scrape data and append tweets to list.
for i,tweet in enumerate(sntwitter.TwitterSearchScraper(
        'Covid-19 lang:en since:2021-07-05 until:2021-07-06'
        ).get_items()):
    if i>500:
        break
    attributes_container.append(
        [tweet.user.username, tweet.date, 
         tweet.likeCount, tweet.sourceLabel, tweet.rawContent]
        )
    
# Creating a dataframe to load the list.
tweets_df = pd.DataFrame(
    attributes_container, 
    columns=[
        "User", "Date Created", 
        "Number of Likes", "Source of Tweet", "Tweet"
        ]
    )
del attributes_container

vectorizer = TfidfVectorizer(
    stop_words='english', ngram_range = (2,2), max_df = .9, min_df = .01
    )

X = vectorizer.fit_transform(tweets_df['Tweet'])
feature_names = vectorizer.get_feature_names_out()

dense = X.todense()
denselist = dense.tolist()
df = pd.DataFrame(denselist, columns=feature_names)

df_avg = df.mean(axis=0)

# change the value to black
def black_color_func(
        word, font_size, position,orientation,random_state=None, **kwargs
        ):
    return("hsl(0,100%, 1%)")
# set the wordcloud background color to white
# set max_words to 1000
# set width and height to higher quality, 3000 x 2000
wordcloud = WordCloud(
    background_color="white", 
    width=3000, height=2000, max_words=500
    ).generate_from_frequencies(df_avg)
# set the word color to black
wordcloud.recolor(color_func = black_color_func)
# set the figsize
plt.figure(figsize=[15,10])
# plot the wordcloud
plt.imshow(wordcloud, interpolation="bilinear")
# remove plot axes
plt.xticks([])
plt.yticks([])
plt.title('Covid-19 Bigrams', fontdict={'fontsize': 50})
# save the image
plt.savefig('Covid-19_bigrams.png')
#%%

image = Image.open('Covid-19.png')
image.show()
image = Image.open('Covid19.png')
image.show()
image = Image.open('Coronavirus.png')
image.show()
image = Image.open('Covid-19_stopwords.png')
image.show()
image = Image.open('Covid-19_stemmed.png')
image.show()
image = Image.open('Covid-19_bigrams.png')
image.show()

