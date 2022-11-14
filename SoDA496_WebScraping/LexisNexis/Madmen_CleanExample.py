# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 18:40:45 2021

@author: chase
"""

import pandas as pd
import os
import regex as re
import glob
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image

os.chdir(r'C:\Users\chase\GDrive\GD_Work\SoDA496\SoDA496_WebScraping\LexisNexis')

####################
###Merge Datasets###
####################

print('Merging Datasets')

path = r'C:\Users\chase\GDrive\GD_Work\SoDA496\SoDA496_WebScraping\LexisNexis'  
all_files = glob.glob(os.path.join(path , "*.csv"))

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)

df = pd.concat(li, axis=0, ignore_index=True)

# ResultId, Link, Source.Name, Document.Content
df_full = df[
    ['ResultId','Title','Date','Document.Content','Source.Name','Link']
    ]
df_full_nona = df_full[df_full['Document.Content'].notna()]


################
###Clean Text###
################
print('Datasets Merged, Begin Cleaning Text')


def clean_text(text):
    # Get rid of special characters.
    xmltext = re.sub(u"[^\x20-\x7f]+",u" ",text) 
    # Get rid of everything before <nitf:body.content><bodyText>.
    xml_temp2 = re.sub(r'^.*?<nitf:body.content><bodyText>','', xmltext) 
    # Remove everything after </p></bodyText>. 
    stripped = xml_temp2.split('</p></bodyText>', 1)[0]
    # Remove everything within <>.
    xml_final = re.sub('<[^>]+>', ' ', stripped) 
    return(xml_final)


content_list = df_full_nona['Document.Content'].tolist()
df_cleaned = [clean_text(row) for row in content_list]

df_full_nona['clean_content'] = df_cleaned

df_full_nodups = df_full_nona.drop_duplicates(
    subset = ['Source.Name','clean_content']
    )

# Clean Text with Beautiful Soup.
bs_content = []
for s in content_list:
    body = []
    soup = BeautifulSoup(s, 'html.parser').find_all("p")
    for p in soup:
        body.append(p.get_text())
    bs_content.append("\n".join(body))
    
# Vectorize and encode text. 
vectorizer = TfidfVectorizer(stop_words='english', 
                             ngram_range = (1,1), 
                             max_df = .9, min_df = .01)
X = vectorizer.fit_transform(bs_content)
feature_names = vectorizer.get_feature_names_out()

# Convert encoded text to term-document frequency matrix. 
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
    width=3000, height=2000, 
    max_words=500
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
plt.title('Madmen', fontdict={'fontsize': 50})
# save the image
plt.savefig('Madmen.png')

image = Image.open('Madmen.png')
image.show()


