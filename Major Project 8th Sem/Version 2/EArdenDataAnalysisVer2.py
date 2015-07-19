# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 14:43:05 2015

@author: Ohm
"""
import pandas as pd
import numpy as np
from pandas import Series, DataFrame

pd.set_option("precision",3)
pd.set_option('max_colwidth',90)
pd.set_option('expand_frame_repr', False)

print "Data Visualization of Income Statement"
print "---------------------------------------"
print ""
print "AVAILABLE ANALYSES:"
print "1. Percentage Change Year-over-Year"
print "2. Percentage Change over any two years"
print "3. Others"
print ""
choice = int(raw_input("Choose your operation: "))
filename = 'Book1.csv'
df1 = pd.read_csv(filename, comment=',')
df1 = df1.dropna(how='all')
df1 = df1.fillna(0)
df2 = DataFrame(df1['Particulars'])
if choice == 1:
    for year_idx in range(1,len(df1.columns[1:])):
        year2 = df1.columns[year_idx]
        year1 = df1.columns[year_idx+1]
        period = 'Period ' + year1[2:] + '-' + year2[2:]
        df2[period] = (df1[year2] - df1[year1])*100
        df2[period] = (df2[period]/df1[year1]).replace({ 0 : np.nan, np.inf : np.nan, -np.inf : np.nan })
elif choice == 2:
    year1 = raw_input("Enter first year: ")
    year2 = raw_input("Enter second year: ")
    period = 'Period ' + year1[2:] + '-' + year2[2:]
    df2[period] = (df1[year2] - df1[year1])*100
    df2[period] = (df2[period]/df1[year1]).replace({ 0 : np.nan, np.inf : np.nan, -np.inf : np.nan })
elif choice == 3:
    pass
else:
    print "Invalid Choice"
df2 = df2.fillna(0)
print ""
print "PARTICULARS OF INCOME STATEMENT:"
print "--------------------------------"
i = 0
for column in df2['Particulars']:
    print str(i) + " " + str(column)
    i =  i + 1
print ""
items = int(raw_input("How many particulars do you wish to see? "))
indexes = []
for i in range(items):
    selection = raw_input("Choose any particular: ")
    indexes.append(int(selection))
df2 = df2.set_index('Particulars')
plot_df = df2.ix[indexes]
print ""
graph = raw_input("Do you wish to see trends format? (Y/N) ")
if graph == 'y' or graph == 'Y':
    plot_df.plot()
else:
    plot_df.plot(kind='barh')