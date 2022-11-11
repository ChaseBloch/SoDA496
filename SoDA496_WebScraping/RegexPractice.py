# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 12:46:30 2022

@author: chase
"""
import regex as re

#https://docs.python.org/3/library/re.html
#https://regexone.com/lesson/introduction_abcs

txt = "The rain in Spain"
re.findall("^The.*Spain$", txt)

txt = "asdfa1lkj4hl65kj7asd8f8k7jhl345kj5678hasd2345fasdf"
re.findall("[0-9]+[a-z]+",txt)


#%%
#Find all occurences of 'rain'
re.findall("rain", txt)
re.findall("Rain", txt)


#Match "asdfa1lkj4hl65kj7asd8f8k7jhl345kj5678hasd2345fasdf"

txt = "asdfa1lkj4hl65kj7asd8f8k7jhl345kj5678hasd2345fasdf"
re.findall("\S*", txt)
re.findall(".*",txt)

#Find the numbers, but not the letters
re.findall("\d", txt)

#Find the letters, but not the numbers
re.findall("\D", txt)

#Match can, man, and fan, but not dan, ran, or pan. 
txt = "can man fan dan ran pan"
re.findall("[cmf]an", txt)

#Match book, look and poof, but not bok, lok, pof, boook, loook, pooof.
txt = "book look poof bok lok pof boook loook pooof"
re.findall("[^o]o{2}[^o]", txt)
#%%