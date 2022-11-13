from dash import Dash, html, dcc
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import json
from pandas import json_normalize
import urllib.request, json 
from datetime import timedelta, datetime
import pytz
import matplotlib.pyplot as plt
import dash_bootstrap_components as dbc
import os

debug = False if os.environ["DASH_DEBUG_MODE"] == "False" else True
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.title = "Electricity-price"

data = urllib.request.urlopen("https://api.energidataservice.dk/dataset/Elspotprices?limit=48&filter={\"PriceArea\":\"DK2\"}").read()
output = json.loads(data)
df = pd.DataFrame(output["records"])
df["price"] = df["SpotPriceEUR"] * 7.44 / 1000.0
df = df[["HourDK", "price"]]

result = []
for value in df["HourDK"]:
    hour = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
    result.append(hour.hour)
df["time"] = result  
result = []
for value in df["HourDK"]:
    hour = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
    result.append(hour.month)
df["month"] = result  
result = []
for value in df["HourDK"]:
    hour = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
    result.append(hour.strftime("%d/%m %H:%M"))
df["timeline"] = result  

#Based on Radius and Modstroem
fixedfee=0.15
electricityfee=0.723
balancetarif=0.00229
systemtarif=0.061
transmissiontarif=0.049
lowconsumption=0.3003
highconsumption=0.7651
vat=1.25


def lowFee(price):
    fee = fixedfee + electricityfee + balancetarif + systemtarif + transmissiontarif + lowconsumption
    pricewithfee = price + fee
    pricewithvatfee = pricewithfee * vat
    return pricewithvatfee

def highFee(price):
    fee = fixedfee + electricityfee + balancetarif + systemtarif + transmissiontarif + highconsumption
    pricewithfee = price + fee
    pricewithvatfee = pricewithfee * vat
    return pricewithvatfee


def currentTime():
    tz_Copenhagen = pytz.timezone('Europe/Copenhagen')
    datetime_Copenhagen = datetime.now(tz_Copenhagen)
    currenttime = datetime_Copenhagen.strftime("%Y-%m-%dT%H:00:00")
    return currenttime

def nextDay():
    tz_Copenhagen = pytz.timezone('Europe/Copenhagen')
    datetime_Copenhagen = datetime.now(tz_Copenhagen)
    tomorrow = datetime.today() + timedelta(1)
    nextDay = tomorrow.strftime("%Y-%m-%dT%00:00:00")
    return nextDay

def attachFee (row):
    if row['peakfee'] == True :
        price = row['price']
        newprice = highFee(price) 
        return newprice
    else :
        price = row['price']
        newprice = lowFee(price)
        return newprice


result = []
for value in df["time"]:
    if 17 <= value <= 20:
        result.append("True")
    else:
        result.append("False")
df["peaktime"] = result  
result = []
for value in df["month"]:
    if 4 <= value <= 9:
        result.append("False")
    else:
        result.append("True")
df["peakmonth"] = result  
df["peakfee"] = ((df['peaktime']=="True") & (df['peakmonth'] == "True"))
df["feeprice"] = df.apply (lambda row: attachFee(row), axis=1)
df['HourDK'] = pd.to_datetime(df['HourDK'])
df = df[(df['HourDK'] >= pd.to_datetime(currentTime()))]
df = df.round({"feeprice": 1})
df = df.sort_values(by="HourDK")
fig = px.bar(df, x="HourDK", y="feeprice", text="feeprice")
fig.update_layout(xaxis_title='Time', yaxis_title='Price in DKK (incl. all fees and taxes)')
fig.update_traces(marker_color='#AFB3BE')
fig.add_hline(y=1.6, line_dash='dash', line_color="#F1EFF2")
fig.add_vline(x=nextDay())


def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])


colors = {
    'background': '#F1EFF2',
    'text': '#272324',
    'focused' : '#272324'
}

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)


app.layout = html.Div(style={'backgroundColor': colors['background'], 'height':'100%', 'z-index':'1000', 'position':'fixed', 'width':'100%'}, children=[
    


    dbc.Container(
    [
        html.Br()
    ],
    fluid=True,
    ),

    
    html.H1(
        children='Electricity-pricing',
        style={
            'textAlign': 'center'        }
    ),



    html.Div(children='A web application that shows the current electricityprice incl. feels, based on Modstroem variable pricing in CPH.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dbc.Container(
    [
        html.Hr()
    ],
    fluid=True,
    ),

        html.H5(children=str("The current price is ") + str(df.iloc[0]["feeprice"]) + str(" DKK"), style={
        'textAlign': 'center',
        'color': colors['focused']
    }),

    dcc.Graph(
        id='example-graph-2',
        figure=fig
    )

])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8050", debug=debug)

