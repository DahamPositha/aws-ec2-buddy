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


df = read_csv(
    '/Users/dahamp/Documents/msc/research-proj/aws-ec2-buddy/src/predictionModels/dataFiles/spot_history_1.csv')


def get_padded_values(df):
    values = []

    for i in range(5):
        for index, row in df.iterrows():
            values.append(row['SpotPrice'])
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
    response = requests.post("http://54.157.252.170:" + str(port) + "/predictSpotPrice",
                             data=json.dumps({"values": values}), headers=headers)
    predictions = json.loads(response.text).get('predictions')
    return predictions


df_values = get_padded_values(df)

# predicted_df_value = get_tensor_flow_predictions(df_values, 5000)

# create new df
df = DataFrame({'col': df_values})
df.to_csv(
    '/Users/dahamp/Documents/msc/research-proj/aws-ec2-buddy/src/predictionModels/dataFiles/spot_predictions.csv')
print (df)
