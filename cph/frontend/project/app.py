"""
CPH Security Queue
"""
import matplotlib.pyplot as plt
import requests
import json
import pandas as pd
from datetime import datetime, timezone
from pandas import Series
import numpy as np
import streamlit as st
import urllib.request
import altair as alt
import datetime
import calendar
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf
from scipy.stats import t
from sklearn.model_selection import TimeSeriesSplit, train_test_split
from sklearn.metrics import mean_absolute_error
import datetime
from lightgbm import LGBMRegressor
import seaborn as sns
import time as t

@st.experimental_memo
def load_data():
    data = urllib.request.urlopen("https://cphapi.simonottosen.dk/waitingtime?select=id,t2waitingtime,deliveryid").read()
    output = json.loads(data)
    dataframe = pd.DataFrame(output)
    StartTime = dataframe["deliveryid"]
    StartTime = pd.to_datetime(StartTime)
    StartTime = StartTime.apply(lambda t: t.replace(tzinfo=None))
    StartTime = StartTime + pd.DateOffset(hours=2)
    dataframe["Date and time"] = StartTime
    dataframe["Queue"] = dataframe["t2waitingtime"]
    dataframe["Time"] = StartTime.dt.time
    dataframe["Date"] = StartTime.dt.date
    return dataframe

def load_latest():
    data = urllib.request.urlopen("https://cphapi.simonottosen.dk/waitingtime?select=id,t2waitingtime,deliveryid&order=id.desc&limit=2").read()
    output = json.loads(data)
    dataframe = pd.DataFrame(output)
    delta = dataframe["t2waitingtime"][0] - dataframe["t2waitingtime"][1]
    latest = dataframe["t2waitingtime"][0]
    delta = np.int16(delta).item()
    latest = np.int16(latest).item()
    M = ' Minutes'
    latest = (str(latest) + M)
    delta = (str(delta) + M)
    return latest, delta


def load_last_two_hours():
    data = urllib.request.urlopen("https://cphapi.simonottosen.dk/waitingtime?select=t2waitingtime&order=id.desc&limit=24").read()
    output = json.loads(data)
    dataframe = pd.DataFrame(output)
    two_hours_avg = dataframe['t2waitingtime'].to_list()
    def Average(l): 
        avg = sum(l) / len(l) 
        return avg
    average = round(Average(two_hours_avg))
    M = ' Minutes'
    average = (str(average) + M)
    return average    


def findDay(date):
    date = str(date)
    born = datetime.datetime.strptime(date, '%Y-%m-%d').weekday()
    return (calendar.day_name[born])

def new_model(test):
    modeldatetime = test["deliveryid"]
    modeldatetime = pd.to_datetime(modeldatetime)
    test["deliveryid"] = modeldatetime
    test = test.set_index(test.deliveryid)
    test.drop('deliveryid', axis=1, inplace=True)
    test['hour'] = test.index.hour
    test['day'] = test.index.day
    test['month'] = test.index.month
    test['weekday'] = test.index.weekday
    data = urllib.request.urlopen("https://cphapi.simonottosen.dk/waitingtime?select=id,t2waitingtime,deliveryid").read()
    output = json.loads(data)
    dataframe = pd.DataFrame(output)
    StartTime = dataframe["deliveryid"]
    StartTime = pd.to_datetime(StartTime)
    StartTime = StartTime.apply(lambda t: t.replace(tzinfo=None))
    StartTime = StartTime + pd.DateOffset(hours=2)
    dataframe["deliveryid"] = StartTime
    df = dataframe.set_index(dataframe.deliveryid)
    df.drop('deliveryid', axis=1, inplace=True)
    df['hour'] = df.index.hour
    df['day'] = df.index.day
    df['month'] = df.index.month
    df['weekday'] = df.index.weekday
    df.drop(['id'], axis=1, inplace=True)
    X = df.drop('t2waitingtime', axis=1)
    y = df['t2waitingtime']
    X_train = X.iloc[:]
    y_train = y.iloc[:]    
    model = LGBMRegressor(random_state=42)
    model.fit(X_train, y_train)
    predict = model.predict(test)
    return round(predict[0])


st.set_page_config(page_icon="✈️", page_title="CPH Security Queue")


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}

footer {
	
	visibility: hidden;
	
	}
footer:after {
	content:'Made with love by Simon Ottosen'; 
	visibility: visible;
	display: block;
	position: relative;
	#background-color: red;
	padding: 5px;
	top: 2px;
}
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# Using object notation

st.sidebar.header("Get queing time for your upcoming flight")
with st.sidebar.form("Input"):
    date = st.sidebar.date_input(
        "On what date is your flight?")
    time = st.sidebar.time_input('At what time would you expect to arrive at the airport?', help="Usually you should arrive approx. 2 hours before your flight if bringing luggage and 1 hour before if you are only bringing carry-on")
    datetime_queue_input_text = ('You will be flying out at ' + str(time.strftime("%H:%M")) + ' on a ' + str(findDay(date)))
    datetime_queue_input = (str(date) + ' ' + str(time))
    test = pd.DataFrame({'deliveryid': [datetime_queue_input]}) 
    btnResult = st.sidebar.button('Calculate expected security queue')

if btnResult:
    with st.sidebar:
        with st.spinner('Estimating queue...'):
            t.sleep(2)
        prediction = new_model(test)
        st.subheader('Expected queue at ' + str(time.strftime("%H:%M")) + ' on a ' + str(findDay(date)) + ' is ' + str(prediction) + ' minutes ✈️')

dataframe = load_data()
currenttime = load_latest()
average = load_last_two_hours()
st.title("✈️ CPH Security Queue")
col1, col2 = st.columns(2)
col1.metric(label="Current waiting time", value=currenttime[0], delta=currenttime[1], delta_color="inverse")
col2.metric(label="Average waiting time in last 2 hours", value=average)

st.line_chart(dataframe, x="Date and time", y="Queue", )