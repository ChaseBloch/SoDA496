library(countrycode) #Do this when you get to merge section
library(stargazer)#DO this during regression output step
library(httr)

#Importing Data
setwd("C:\\Users\\chase\\GDrive\\GD_Work\\SoDA496\\CodingIntro\\")
Polity = read.csv("PolityV.csv")
WorldBank = read.csv("WB_Emissions.csv")

#Clean Polity Data
pv = Polity[c('ccode','scode','country','year','polity')]
pv = pv[pv$year >=1990,]
pv = pv[pv$polity >= -10,] #Do this after visualization step

#Clean Worldbank Data
wb = WorldBank
colnames(wb)[5] = "NO2"
colnames(wb)[6] = "CO2"
colnames(wb)[7] = "CH4"
wb[c("Time","CO2", "NO2", "CH4")] = lapply(wb[c("Time","CO2", "NO2", "CH4")], as.numeric) #Do this after visualization step
wb$Time.Code = NULL
wb = na.omit(wb) 

#Visualize Data
hist(pv$polity)

hist(wb$CO2)
class(wb$CO2)
as.numeric(wb$CO2)

hist(wb$NO2)
hist(wb$NO2[wb$Time > 2015])

#Check Overlaps  (First compare country codes, then compare country names (Burkina Faso, Congo))
pv$Country.Code = countrycode(pv$scode,"cowc","iso3c") #Remember to check error message

write.csv(pv, "pv_cleaned.csv")

for(i in 1:length(pv$Country.Code)){
  if(is.na(pv$Country.Code[i])){
    pv$Country.Code[i] = pv$scode[i]
  }
}

setdiff(pv$Country.Code,wb$Country.Code)



#Merge  https://shanelynnwebsite-mid9n9g1q9y8tt.netdna-ssl.com/wp-content/uploads/2017/03/join-types-merge-names.jpg
df = merge(pv, wb, by.x = c("Country.Code", "year"), by.y = c("Country.Code", "Time"))

#Scatter plot
plot(df$polity, df$NO2)
plot(df$polity, df$CO2)
plot(df$polity, df$CH4)

#Regression model
m1 = lm(CO2 ~ poly(polity,2), data = df)
summary(m1)

m2 = lm(NO2 ~ poly(polity,2), data = df)
m3 = lm(CH4 ~ poly(polity,2), data = df)

#Output Regression
stargazer(m1,m2,m3, type = "html", out = "model.html",
          covariate.labels = c("Polity","Polity\\^2", NA),
          dep.var.labels = c("CO2","NO2", "CH4"),
          omit.stat = c("ser", "f","adj.rsq"))
BROWSE("model.html")

##Testing Git with R in VSCode
##Test with Git 2
##Test 3
