#!/usr/bin/env python

from pandas import read_csv
from matplotlib import pyplot
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
import time
from dateutil import parser as date_parser
import datetime
import requests
import json
import numpy as np


def parser(x):
    return x

df = read_csv('/Users/dahamp/Documents/msc/research-proj/aws-ec2-buddy/src/predictionModels/dataFiles/spot_history_1.csv')

dict ={}
val_points=[]
values=[]

for index, row in df.iterrows() :
    dt=date_parser.parse(row['Timestamp'])
    unixtime=time.mktime(dt.timetuple())
    key=int(unixtime/(3600*24))
    val_points.append(key)

    if dict.get(key) is not None:
        if row['SpotPrice'] > dict[key]:
            dict[key]=row['SpotPrice']
            continue
    dict[key]=row['SpotPrice']

print(len(val_points))
val_points.reverse()


t=val_points[0]
prev=dict.get(t)

key_val_dict={}

while t <= val_points[len(val_points)-1]:
    if dict.get(t) is not None:
        values.append(dict.get(t))
        prev=dict.get(t)
        key_val_dict[datetime.datetime.fromtimestamp(t*3600*24).strftime('%Y-%m-%d %H:%M:%S')]=dict.get(t)
    else:
        values.append(prev)
        key_val_dict[datetime.datetime.fromtimestamp(t*3600*24).strftime('%Y-%m-%d %H:%M:%S')]=prev
    t=t+1

print(key_val_dict)
print(values)


headers = {'content-type': 'application/json'}
response = requests.post("http://54.157.252.170:" + str(5000) + "/predictSpotPrice",
                             data=json.dumps({"values": values}), headers=headers)

print(response.text)
test=json.loads(response.text).get('test')

predictions=json.loads(response.text).get('predictions')

pyplot.plot(values)

x_range = np.arange((len(values)-len(predictions)-1),(len(values)-1))
pyplot.plot(x_range,predictions)
pyplot.show()


