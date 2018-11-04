from pandas import read_csv, DataFrame
from matplotlib import pyplot
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
import time
from dateutil import parser as date_parser
import datetime
from math import sqrt
import requests
import numpy as np
import json


def parser(x):
    return x


df1 = read_csv('/Users/dahamp/Documents/msc/research-proj/aws-ec2-buddy/src/predictionModels/dataFiles/spot_history_1.csv')
df2 = read_csv('/Users/dahamp/Documents/msc/research-proj/aws-ec2-buddy/src/predictionModels/dataFiles/spot_history_2.csv')


def get_padded_values(df):
    dict = {}
    val_points = []
    values = []

    for index, row in df.iterrows():
        dt = date_parser.parse(row['Timestamp'])
        unixtime = time.mktime(dt.timetuple())
        key = int(unixtime / (3600 * 24))
        val_points.append(key)

        if dict.get(key) is not None:
            if row['SpotPrice'] > dict[key]:
                dict[key] = row['SpotPrice']
                continue
        dict[key] = row['SpotPrice']

    print(len(val_points))
    val_points.reverse()

    t = val_points[0]
    prev = dict.get(t)

    key_val_dict = {}

    while t <= val_points[len(val_points) - 1]:

        if dict.get(t) is not None:
            values.append(dict.get(t))
            prev = dict.get(t)
            key_val_dict[datetime.datetime.fromtimestamp(t * 3600 * 24).strftime(
                    '%Y-%m-%d %H:%M:%S')] = dict.get(t)
            print(
                datetime.datetime.fromtimestamp(t * 3600 * 24).strftime('%Y-%m-%d %H:%M:%S'),
                dict.get(t))
        else:
            values.append(prev)
            key_val_dict[
                datetime.datetime.fromtimestamp(t * 3600 * 24).strftime('%Y-%m-%d %H:%M:%S')] = prev
            print(
                datetime.datetime.fromtimestamp(t * 3600 * 24).strftime('%Y-%m-%d %H:%M:%S'), prev)
        t = t + 1
    return values


def get_arima_predictions(values):
    size = int(len(values) * 0.66)
    train, test = values[0:size], values[size:len(values)]
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
    error = mean_squared_error(test, predictions)
    print('Test MSE: %.3f' % error)

    return predictions

def get_tensor_flow_predictions(values, port):
    headers = {'content-type': 'application/json'}
    response = requests.post("http://54.157.252.170:"+str(port)+"/predictSpotPrice", data=json.dumps({"values":values}), headers=headers)
    predictions=json.loads(response.text).get('predictions')
    return predictions


doubled_df1_values = [i * 3 for i in get_padded_values(df1)]
df2_values = get_padded_values(df2)

#create new df
df = DataFrame({'col':df2_values})
df.to_csv('/Users/dahamp/Documents/msc/research-proj/aws-ec2-buddy/src/predictionModels/dataFiles/spot_predictions.csv')
print (df)

pyplot.plot(doubled_df1_values)
pyplot.plot(df2_values)

predicted_doubled_df1_values = get_tensor_flow_predictions(doubled_df1_values,5000)
predicted_df2_value = get_tensor_flow_predictions(df2_values,5001)

min_of_preds=[min(x,y) for x, y in zip(predicted_doubled_df1_values, predicted_df2_value)]
print(min_of_preds)

x_range = np.arange((len(doubled_df1_values) - len(min_of_preds) - 1), (len(doubled_df1_values) - 1))
pyplot.plot(x_range, min_of_preds)

pyplot.show()


#create new df
df = DataFrame({'col':predicted_df2_value})
df.to_csv('/Users/dahamp/Documents/msc/research-proj/aws-ec2-buddy/src/predictionModels/dataFiles/spot_predictions.csv')
print (df)
