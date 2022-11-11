#https://cran.r-project.org/web/packages/stringr/vignettes/regular-expressions.html
#https://regexone.com/lesson/introduction_abcs

library(stringr)

txt = "The rain rain in Spain"
str_extract(txt, "^The.*Spain$")

#####
#Find all occurences of 'rain'
str_extract_all(txt, "rain")
str_extract(txt, "Rain")

txt = "asdfa1lkj4hl65kj7asd8f8k7jhl345kj5678hasd2345fasdf"




























#Match "asdfa1lkj4hl65kj7asd8f8k7jhl345kj5678hasd2345fasdf"

txt = "asdfa1lkj4hl65kj7asd8f8k7jhl345kj5678hasd2345fasdf"
str_extract_all(txt,"\\S*")

#Find the numbers, but not the letters
str_extract_all(txt, "\\d")

#Find the letters, but not the numbers
str_extract_all(txt,"\\D")

#Match can, man, and fan, but not dan, ran, or pan. 
txt = "can man fan dan ran pan"
str_extract_all(txt, "[cmf]an")

#Match book, look and poof, but not bok, lok, pof, boook, loook, pooof.
txt = "book look poof bok lok pof boook loook pooof"
str_extract_all(txt, "[^o]o{2}[^o]")
#%%
#####