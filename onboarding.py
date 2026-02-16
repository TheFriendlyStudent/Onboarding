# DFR Onboarding Project

from dash import Dash, dcc, html, Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import numpy as np

#import the data and drop columns with only one unique value to clean up data
data = pd.read_csv('can_data.csv', on_bad_lines='skip')

for each in data.columns:
    data[each] = data[each].dropna()
    if data[each].nunique() == 1:
        data = data.drop(columns=[each])

#drop rows with NaN values and convert UNIX timestamps to datetime for readability
data = data.dropna(how="any")
data["timestamp"] = pd.to_datetime(data["timestamp"], unit="s")

#smoothing the speed data for better readability 
#calculating acceleration by taking derivative of speed over time
speed_converted = data["Driven Avg Wheel Speed"] / 3.6
speed_mps_smooth = speed_converted.rolling(25, center=True).mean()

#adding the new values to the dataframe
data["Accel"] = speed_mps_smooth.diff() / data["timestamp"].diff().dt.total_seconds()

#setting up the plotly graph and dash app to display data
app = Dash(__name__)

#creating dropdowns to toggle visibility of the two graphs
app.layout = html.Div([
    html.H4('Data Visualization: DFR Onboarding Project'),
    html.P("Select color:"),
    html.P("Show Acceleration:"),
    dcc.Dropdown(
        id="dropdown2",
        options=[True, False],
        value=True,
        clearable=False,
    ),html.P("Show Analog 2:"),
    dcc.Dropdown(
        id="dropdown3",
        options=[True, False],
        value=True,
        clearable=False,
    ),
    dcc.Graph(id="graph"),
])

#produce two graphs plotting two inputs over time
#runtime code to update the graph based on dropdown selections
@app.callback(
    Output("graph", "figure"))
def display_color():

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        subplot_titles=("Analog Input #2", "Acceleration")
    )

    # Top chart
    fig.add_trace(
        go.Scatter(
            x=data["TPS"],
            y=data["Fuel Open Time"],
            mode="lines",
            name="Analog Input #2"
        ),
        row=1,
        col=1
    )

    # Bottom chart
    fig.add_trace(
        go.Scatter(
            x=data["timestamp"],
            y=data["Accel"],
            mode="lines",
            name="Acceleration"
        ),
        row=2,
        col=1
    )

    fig.update_layout(
        height=700,
        title="Acceleration vs Time",
        showlegend=True
    )

    return fig

app.run(debug=True)