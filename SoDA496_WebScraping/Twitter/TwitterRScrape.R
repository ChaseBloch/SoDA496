library(dplyr)
library(twitteR)
library(rtweet)

#####
API_key = ''
API_secret = ''
Access_token = ''
Access_secret = ''
######

setup_twitter_oauth(API_key,API_secret,Access_token,Access_secret)


###https://jtr13.github.io/cc21fall2/scrape-twitter-data-using-r.html 
###Using twitteR###

covid_raw <- searchTwitter("Covid-19", n=500, lang="en", since="2022-10-24", until="2022-10-25" )
covid_df <- covid_raw %>% 
  strip_retweets() %>%  #Gets rid of retweets
  twListToDF() #Assigns tweets to a dataframe


knitr::kable(covid_df[1:3,], format="markdown")

####Using Rtweet###
#auth_setup_default()

covid_df2 <- search_tweets("Covid-19 vaccine flu",n=150, include_rts=FALSE, lang="en")
