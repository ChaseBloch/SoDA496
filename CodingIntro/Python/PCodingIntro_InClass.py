# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import re
import statsmodels.formula.api as sm
import statsmodels.api as SM
from stargazer.stargazer import Stargazer
from IPython.core.display import HTML
import webbrowser

#Importing Data
os.chdir(r"C:\Users\chase\GDrive\GD_Work\SoDA496\CodingIntro")
Polity = pd.read_csv(r"PolityV.csv")
WorldBank = pd.read_csv(r"WB_Emissions.csv")

#Clean Polity Data
pv = Polity[['ccode','scode','country','year','polity']]
pv = pv[pv.year >= 1990]
pv = pv[pv.polity >= -10]

#Clean Worldbank Data
wb = WorldBank
wb.columns = [re.sub(" ","_",c) for c in wb.columns]
wb.columns.values[4] = "NO2"
wb.columns.values[5] = "CO2"
wb.columns.values[6] = "CH4"
wb = wb.replace("..", np.nan)
wb = wb.drop("Time_Code", axis = 1)
wb = wb.dropna()  #dropna(wb)
wb[["Time","CO2", "NO2", "CH4"]] = wb[["Time","CO2", "NO2", "CH4"]].apply(pd.to_numeric)

#Visualize Data
plt.hist(pv.polity)
plt.show()

plt.hist(wb.CO2)

#Merging Data
pv = pd.read_csv(r"pv_cleaned.csv")
pv.columns = [re.sub("\.","_",c) for c in pv.columns]

for i in range(len(pv.Country_Code)):
    if pd.isna(pv.Country_Code[i]):
        pv.Country_Code[i] = pv.scode[i]
        
df = pv.merge(wb, left_on = ("Country_Code", "year"), 
              right_on = ("Country_Code","Time"))

set(pv.Country_Code) ^ set(wb.Country_Code)

plt.scatter(df.polity, df.CO2)

#Regression
df ['polity_2'] = df.polity*df.polity

X = df[["polity","polity_2"]]
y = df["CO2"]

model = sm.ols(formula = "CO2 ~ polity + np.power(polity,2)", data = df).fit()
model = SM.OLS(y,X).fit()

output = Stargazer([model])
table = HTML(output.render_html())

with open("table.html","w") as file:
    file.write(table.data)
    
webbrowser.open('table.html')








