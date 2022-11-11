library(countrycode)
library(stargazer)
library(httr)

###Importing Data###
setwd("C:\\Users\\chase\\GDrive\\GD_Work\\SoDA496\\CodingIntro\\") 
PolityV = read.csv("PolityV.csv")
WorldBank = read.csv("WB_Emissions.csv")

#Clean
pv = PolityV[c("ccode","scode","country","year", "polity")]
pv = pv[pv$year >= 1990,]
pv = pv[pv$polity >= -10,]


#Clean World Bank Data
wb = WorldBank
colnames(wb)[6] = "CO2"
wb[c("Time","CO2")] = lapply(wb[c("Time","CO2")], as.numeric)
wb$Time.Code = NULL
wb = na.omit(wb)

#Visualize Data
hist(pv$polity)

hist(wb$CO2[wb$Time > 2016])

pv$Country.Code = countrycode(pv$scode, "p4c", "iso3c")      







for(i in 1:length(pv[[1]])){
  if(is.na(pv$Country.Code[i])){
    pv$Country.Code[i] = pv$scode[i]
  }
}

setdiff(pv$Country.Code, wb$Country.Code)

df = merge(pv, wb, by.x = c("Country.Code", "year"), by.y = c("Country.Code", "Time"))

#Scatter Plot
plot(df$polity, df$CO2)

m1 = lm(CO2 ~ poly(polity, 2), data = df)
summary(m1)

stargazer(m1, type = "html", out = "model.html",
          covariate.labels = c("Polity", "Polity\\^2",NA),
          dep.var.labels = c("CO2"),
          omit.stat = c("ser", "f","adj.rsq"))

BROWSE("model.html")

