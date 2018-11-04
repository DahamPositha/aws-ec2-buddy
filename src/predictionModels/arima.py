from pandas import read_csv, DataFrame
from matplotlib import pyplot
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
import time
from dateutil import parser as date_parser
import datetime
from math import sqrt
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error

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
        print(datetime.datetime.fromtimestamp(t*3600*24).strftime('%Y-%m-%d %H:%M:%S'),dict.get(t))
    else:
        values.append(prev)
        key_val_dict[datetime.datetime.fromtimestamp(t*3600*24).strftime('%Y-%m-%d %H:%M:%S')]=prev
        print(datetime.datetime.fromtimestamp(t*3600*24).strftime('%Y-%m-%d %H:%M:%S'),prev)
    t=t+1

print(key_val_dict)

size = int(len(values) * 0.66)
train, test = values[0:size], values[size:len(values)]

print train

#create new df
df = DataFrame({'col':train})
#df.to_csv('/Users/dahamp/Documents/msc/research-proj/aws-ec2-buddy/src/predictionModels/dataFiles/spot_predictions.csv')
print (df)

history = [x for x in train]
predictions = list()

for t in range(len(test)):
    model = ARIMA(history, order=(5, 1, 0))
    model_fit = model.fit(disp=0)
    output = model_fit.forecast()
    yhat = output[0]
    predictions.append(yhat)
    obs = test[t]
    history.append(obs)
    print('predicted=%f, expected=%f' % (yhat, obs))
mse = mean_squared_error(test, predictions)
mae = mean_absolute_error(test, predictions)
print('MSE: %f' % mse)
print('RMSE: %f' % sqrt(mse))
print('MAE: %f' % sqrt(mae))



pyplot.plot(values)

x_range = np.arange((len(values)-len(predictions)-1),(len(values)-1))
pyplot.plot(x_range,predictions)
pyplot.show()