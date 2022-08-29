"""
CPH Security Queue
"""
import matplotlib.pyplot as plt
import psycopg2
import requests
import json
from datetime import datetime
import pandas as pd
from datetime import datetime, timezone
from pandas import Series
import numpy as np
import streamlit as st


@st.experimental_memo
def load_data():
    try:
        connection = psycopg2.connect(user="postgres",
                                    password="postgres",
                                    host="cph_postgres_db",
                                    port="5432",
                            
                                    database="postgres")
        cursor = connection.cursor()
        postgreSQL_select_Query =    "SELECT * FROM waitingtime"

        cursor.execute(postgreSQL_select_Query)
        print("Selecting rows from waitingtime table using cursor.fetchall")
        waitingtime = cursor.fetchall()

        print("Print each row and it's columns values")
        #for row in waitingtime:
        #    print("Id = ", row[0], )
        #    print("t2WaitingTime = ", row[1])
        #    print("t2WaitingTimeInterval = ", row[2])
        #    print("deliveryId  = ", row[3], "\n")

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
    dataframe = pd.DataFrame(waitingtime,columns=['ID', 'Waitingtime', 'MintoMMax', 'Timestamp'])
    StartTime = dataframe["Timestamp"]
    StartTime = pd.to_datetime(StartTime)
    StartTime = StartTime.apply(lambda t: t.replace(tzinfo=None))
    StartTime = StartTime + pd.DateOffset(hours=2)
    dataframe["Timestamp"] = StartTime
    dataframe["Time"] = StartTime.dt.time
    dataframe["Date"] = StartTime.dt.date
    return dataframe

df = load_data()
st.title("CPH Security Queue")

st.write("Overview of data:")
st.write(
    pd.DataFrame(df)
)
dfchart = pd.concat(df['Waitingtime'], [df['Timestamp']], axis=1, keys=['Waitingtime', 'Timestamp'])
st.line_chart(dfchart)