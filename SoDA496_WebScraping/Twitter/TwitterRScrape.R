library(dplyr)
library(twitteR)
library(rtweet)

#####
API_key = 'F4mASP12B1oaWjrnjXGI2Xz4K'
API_secret = '0NYpbio5ELLIDHMKUG1SheYZrMQU5vO8QfcoiscMZlRWMO9PTn'
Access_token = '1057441879523057669-yispuKmbRB4IA7Dc8IyOH1ZwzCb9Lb'
Access_secret = 'b2g9KikltoYAwQJht0jdiFWb6wvnrHaEQ8RjPa7d6Zzk3'
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