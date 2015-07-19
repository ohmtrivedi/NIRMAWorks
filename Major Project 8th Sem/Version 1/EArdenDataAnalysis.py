# -*- coding: utf-8 -*-
"""
Created on Tue Jun 09 09:07:40 2015

@author: Ohm
"""
import pandas as pd
from pandas import Series, DataFrame
#import matplotlib.pyplot as plt

filename = 'Book2.csv'
df = pd.read_csv(filename,index_col='Periods')

print "Data Visualization of Income Statement"
print "---------------------------------------"
print ""
print "Particulars of Income Statement:"
i = 0
for column in df.columns:
    print str(i) + " " + column
    i =  i + 1
print ""
no = raw_input("Do you wish to see all of them (Press 1) or only some (Press 2)? ")
if no == '1':
    df.plot(title='% Change in Quantities Year-over-Year')
elif no == '2': 
    items = int(raw_input("How many particulars do you wish to see? "))
    indexes = []
    for count in range(items):
        selection = raw_input("Choose any particular: ")
        if selection < 0 or selection > i:
            print "Invalid choice. Re-enter."
            selection = raw_input("Choose any particular: ")
        indexes.append(int(selection))
    plot_df = df[indexes]
    plot_df.plot(title='% Change in Quantities Year-over-Year')
else:
    print "Invalid Entry."