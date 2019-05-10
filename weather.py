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

app = dash.Dash()

app.layout = html.Div([
        html.Iframe(src = 'https://www.accuweather.com/en/eg/cairo/127164/weather-forecast/127164',
        height = 500, width = 1200)
        ])


if __name__ == '__main__':
    app.run_server()
