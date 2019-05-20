'''
This a dash application to scrapping the weather data for selected region
and place.
'''
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import requests
import pandas as pd
import time
import scrapping

# intitial scrapping for countries
countries = scrapping.Countries()
# select initial country
country = {'country':countries['country'][0],'link':countries['link'][0]}
# pause for 1 second to avoid web blocking
time.sleep(1)
# intitial cities scrapping for selected country
cities = scrapping.Cities(country)
# select initial city
city = {'city':cities['city'][0],'link':cities['link'][0]}
# pause for 1 second to avoid web blocking
time.sleep(1)
# weather scrapping for selected city
weather = scrapping.City(city)

# create dash application
app = dash.Dash()

# create dash layout
app.layout = html.Div([
    html.Div([ html.H1(children='Weather Scrapping for weather-forecast.com',
        style={'textAlign': 'center'}),
        html.Div([ html.H3(children='Select Country: ',
            style={'width': '30%'}),
            dcc.Dropdown(
                id='country-id',
                options=[{'label': i, 'value': i} for i in countries['country']],
                value=countries['country'][0]
            )], style={'width': '30%'}),
        html.Div([html.H3(children='Select City: ',
            style={'width': '30%'}),
            dcc.Dropdown(
                id='city-id',
                options=[{'label': i, 'value': i} for i in cities['city']],
                value=cities['city'][0]
            )], style={'width': '30%'}),
        html.Div([ html.Br(),
            html.Button(
                id='submit-button',
                n_clicks=0,
                children='Submit',
                style={'fontSize':28}
            )], style={'width': '30%'}),
    ], style={'padding':10}),
    html.Div([
        dcc.Graph(id='weather-plot')
        ], style={'width':'90%', 'float':'center'}),
])

@app.callback(Output('city-id','options'),[Input('country-id','value')])
def cities_options(SelectedCountry):
    '''
    Function to get the list of cities for the selected country
    '''
    # use globla cities variable
    global cities
    # get country data for the selected one
    GetCountry = {'country':SelectedCountry,
            'link':countries['link'][countries.loc[countries.country==SelectedCountry].index[0]]}
    # scrapping the cities for the selected country
    cities = scrapping.Cities(GetCountry)
    # return cities as options for Cities Dropdown
    return [{'label': i, 'value': i} for i in cities['city']]

@app.callback(Output('city-id','value'),[Input('city-id','options')])
def cities_value(SelectedCities):
    '''
    Function to set the first city on the list as a value
    '''
    return cities['city'][0]

@app.callback(
    Output('weather-plot', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [State('city-id', 'value')])
def update_graph(n_clicks,SelectedCity):
    '''
    Function to get the weather details for the selected city
    and return graph data
    '''
    global weather
    # get city data for the selected one
    GetCity = {'city':SelectedCity,
        'link':cities['link'][cities.loc[cities.city==SelectedCity].index[0]]}
    # scrapping weather data for the selected city
    weather = scrapping.City(GetCity)
    # change dates colum type to string instead of number
    weather['dates']=pd.Series(weather['dates'],dtype=str)

    # create traces for AM times
    AmHigh = go.Scatter(x=weather[weather['time'] == 'AM']['dates'] + ' - '
                        + weather[weather['time'] == 'AM']['days'],
                        y=weather[weather['time'] == 'AM']['HighTemp'],
                        mode='lines',name='High Temperatures at AM')
    AmLow = go.Scatter(x=weather[weather['time'] == 'AM']['dates'] + ' - '
                        + weather[weather['time'] == 'AM']['days'],
                        y=weather[weather['time'] == 'AM']['LowTemp'],
                        mode='lines',name='Low Temperatures at AM')
    # create traces for PM times
    PmHigh = go.Scatter(x=weather[weather['time'] == 'PM']['dates'] + ' - '
                        + weather[weather['time'] == 'PM']['days'],
                        y=weather[weather['time'] == 'PM']['HighTemp'],
                        mode='lines',name='High Temperatures at PM')
    PmLow = go.Scatter(x=weather[weather['time'] == 'PM']['dates'] + ' - '
                        + weather[weather['time'] == 'PM']['days'],
                        y=weather[weather['time'] == 'PM']['LowTemp'],
                        mode='lines',name='Low Temperatures at PM')
    # create traces for NIGHT times
    NightHigh = go.Scatter(x=weather[weather['time'] == 'NIGHT']['dates'] + ' - '
                            + weather[weather['time'] == 'NIGHT']['days'],
                            y=weather[weather['time'] == 'NIGHT']['HighTemp'],
                            mode='lines',name='High Temperatures at NIGHT')
    NightLow = go.Scatter(x=weather[weather['time'] == 'NIGHT']['dates'] + ' - '
                            + weather[weather['time'] == 'NIGHT']['days'],
                            y=weather[weather['time'] == 'NIGHT']['LowTemp'],
                            mode='lines',name='Low Temperatures at NIGHT')
    # list all traces on data list
    data = [AmHigh, AmLow, PmHigh, PmLow, NightHigh, NightLow]
    # create graph layout
    layout = go.Layout(title = '{0} Weather for 9 days'.format(SelectedCity),
                    xaxis = {'title': 'Days'},
                    yaxis = {'title': 'Temperatures C'},
                    hovermode='closest'
                    )
    # return graph figure
    return {'data':data, 'layout':layout}

if __name__ == '__main__':
    app.run_server()
