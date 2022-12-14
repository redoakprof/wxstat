from matplotlib import pyplot
import numpy as np
import pandas as pd
import csv
import datetime
import socket
import config

# read actuals into a dict (round the temp to zero decimal digits)
 
actuals_high = {}
actuals_low = {}
fcast = []
fcasts = []
row_count = 0

# open actuals file and store highs and lows in separate dicts
# with date as key for each

f_act = config.CSVActuals
with open(f_act) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        row_count += 1
        actuals_high[datetime.datetime.strptime(row[1], "%Y-%m-%d")] = row[2]
        actuals_low[datetime.datetime.strptime(row[1], "%Y-%m-%d")] = row[3]

print('Read ' + str(row_count) + ' rows from actuals.csv')
row_count = 0

# open fcasts CSV and store rows in list of lists fcasts
        
f_fct = config.CSVFcasts
with open(f_fct) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        fcast.append(datetime.datetime.strptime(row[1],"%Y-%m-%d"))
        fcast.append(datetime.datetime.strptime(row[2],"%Y-%m-%d"))
        fcast.append(row[3])
        fcast.append(row[4])
        fcasts.append(fcast)
        fcast = []
        row_count += 1

print('Read ' + str(row_count) + ' rows from fcasts.csv')
row_count = 0

# initialize the data list of lists for each of high and low
# format then the first index key is days between actual and origin of forecast date
# should have a max of difference max_diff

max_diff = 10
data_high = []
data_low = []
data_out = []
for i in range(max_diff):
    data_high.append([])
    data_low.append([])

f_do = config.CSVDataOut
f = open(f_do, 'w')
writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_ALL)

for row in fcasts:
    if row[2] == "High":
        if row[0] in actuals_high.keys():
            data_out.append(row[0])
            data_out.append(row[1])
            data_out.append(row[3])
            data_out.append('High')
            data_out.append(actuals_high[row[0]])
            writer.writerow(data_out)
            data_out= []
            row_count += 1
            data_high[(row[0]-row[1]).days].append(round(float(row[3]) - \
                                                         float(actuals_high[row[0]]), 2))
    elif row[2] == "Low":
        if row[0] in actuals_low.keys():
            data_out.append(row[0])
            data_out.append(row[1])
            data_out.append(row[3])
            data_out.append('Low')
            data_out.append(actuals_low[row[0]])
            writer.writerow(data_out)
            data_out = []
            row_count += 1
            data_low[(row[0]-row[1]).days].append(round(float(row[3]) -
                                                        float(actuals_low[row[0]]), 2))
f.close()

print('Wrote ' + str(row_count) + ' rows to data_out.csv')
print('Data available for plotting :')
print('HIGH -->')
for item in data_high:
    print('- ' + str(item))
print('LOW -->')
for item in data_low:
    print('- ' + str(item))

num_bins = 20
mint = -15
maxt = 15

f, a = pyplot.subplots(4, 1, sharex = True)
f.suptitle('High Diffs')
a = a.ravel()

for idx, ax in enumerate(a):
    ax.set_title(idx)
    ax.hist(data_high[idx], num_bins)

pyplot.xlim([mint,maxt])
pyplot.tight_layout()
pyplot.savefig(config.PNGHistHigh)
print('Saved High Histograms')

f, a = pyplot.subplots(4, 1, sharex = True)
f.suptitle('Low Diffs')
a = a.ravel()

for idx, ax in enumerate(a):
    ax.set_title(idx)
    ax.hist(data_low[idx], num_bins)

pyplot.xlim([mint,maxt])
pyplot.tight_layout()
pyplot.savefig(config.PNGHistLow)
print('Saved Low Histograms')
