'''
This a dash application to scrapping the weather data for selected region
and place.
'''
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import requests
import pandas as pd
import time
import scrapping

countries = scrapping.Countries()
country = {'country':countries['country'][0],'link':countries['link'][0]}
time.sleep(1)
cities = scrapping.Cities(country)
city = {'city':cities['city'][0],'link':cities['link'][0]}
time.sleep(1)
weather = scrapping.City(city)

app = dash.Dash()

app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='country-id',
                options=[{'label': i, 'value': i} for i in countries['country']],
                value=countries['country'][0]
            )], style={'width': '30%', 'display': 'inline-block'}),
        html.Div([
            dcc.Dropdown(
                id='city-id',
                options=[{'label': i, 'value': i} for i in cities['city']],
                value=cities['city'][0]
            )], style={'width': '30%', 'display': 'inline-block'}),
        html.Div([
            html.Button(
                id='submit-button',
                n_clicks=0,
                children='Submit',
                style={'fontSize':28}
            )], style={'width': '30%', 'display': 'inline-block'}),
    ], style={'padding':10}),
    html.Div([
        dcc.Graph(
            id='weather-plot',
            figure={
                'data': [
                    go.Scatter(
                        x = weather['days'],
                        y = weather['HighTemp'],
                        mode='markers'
                    )
                ],
                'layout': go.Layout(
                    title = 'Weather for nine days',
                    xaxis = {'title': 'Days'},
                    yaxis = {'title': 'Temperatures'},
                    hovermode='closest'
                )
            }
        )], style={'width':'90%', 'float':'center'}),
])
@app.callback(Output('city-id','options'),[Input('country-id','value')])
def cities_options(SelectedCountry):
    global cities
    GetCountry = {'country':SelectedCountry,
            'link':countries['link'][countries.loc[countries.country==SelectedCountry].index[0]]}
    cities = scrapping.Cities(GetCountry)
    return [{'label': i, 'value': i} for i in cities['city']]

@app.callback(Output('city-id','value'),[Input('city-id','options')])
def cities_value(SelectedCities):
    return cities['city'][0]

@app.callback(
    Output('weather-plot', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [State('city-id', 'value')])
def update_graph(SelectedCity):
    

if __name__ == '__main__':
    app.run_server()
