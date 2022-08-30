"""
CPH Security Queue
"""
import matplotlib.pyplot as plt
import requests
import json
from datetime import datetime
import pandas as pd
from datetime import datetime, timezone
from pandas import Series
import numpy as np
import streamlit as st
import urllib.request
import altair as alt
from bokeh.plotting import figure

@st.experimental_memo
def load_data():
    data = urllib.request.urlopen("https://cphapi.simonottosen.dk/waitingtime?select=id,t2waitingtime,deliveryid").read()
    output = json.loads(data)
    dataframe = pd.DataFrame(output)
    StartTime = dataframe["deliveryid"]
    StartTime = pd.to_datetime(StartTime)
    StartTime = StartTime.apply(lambda t: t.replace(tzinfo=None))
    StartTime = StartTime + pd.DateOffset(hours=2)
    dataframe["deliveryid"] = StartTime
    dataframe["Time"] = StartTime.dt.time
    dataframe["Date"] = StartTime.dt.date
    return dataframe

def load_latest():
    data = urllib.request.urlopen("https://cphapi.simonottosen.dk/waitingtime?select=id,t2waitingtime,deliveryid&order=id.desc&limit=2").read()
    output = json.loads(data)
    dataframe = pd.DataFrame(output)
    StartTime = dataframe["deliveryid"]
    StartTime = pd.to_datetime(StartTime)
    StartTime = StartTime.apply(lambda t: t.replace(tzinfo=None))
    StartTime = StartTime + pd.DateOffset(hours=2)
    dataframe["deliveryid"] = StartTime
    dataframe["Time"] = StartTime.dt.time
    dataframe["Date"] = StartTime.dt.date
    delta = dataframe["t2waitingtime"][0] - dataframe["t2waitingtime"][1]
    latest = dataframe["t2waitingtime"][0]
    delta = np.int16(delta).item()
    latest = np.int16(latest).item()
    M = ' Minutes'
    latest = (str(latest) + M)
    return latest, delta

    

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



df = load_data()
currenttime = load_latest()
st.title("CPH Security Queue")
st.metric(label="Current waiting time", value=currenttime[0], delta=currenttime[1])

p = figure(
     title='Overview of CPH queuing time',
     x_axis_type='datetime',
     x_axis_label='Time',
     y_axis_label='Queue')

p.line(df["deliveryid"], df["t2waitingtime"], legend_label='Trend', line_width=2)

st.bokeh_chart(p, use_container_width=True)
st.dataframe(df)

