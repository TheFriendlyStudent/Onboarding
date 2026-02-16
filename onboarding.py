# DFR Onboarding Project

from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd
import numpy as np

#import the data and drop columns with only one unique value to clean up data
data = pd.read_csv('can_data.csv', on_bad_lines='skip')

print(data.head(10000))

for each in data.columns:
    data[each] = data[each].dropna()
    if data[each].nunique() == 1:
        data = data.drop(columns=[each])

#drop rows with NaN values and convert UNIX timestamps to datetime for readability
data = data.dropna(how="any")
data["timestamp"] = pd.to_datetime(data["timestamp"], unit="s")

speed_converted = data["Driven Avg Wheel Speed"] / 3.6
speed_mps_smooth = speed_converted.rolling(10, center=True).mean()
data["Accel"] = speed_mps_smooth.diff() / data["timestamp"].diff().dt.total_seconds()

#setting up the plotly graph and dash app to display data
app = Dash(__name__)


app.layout = html.Div([
    html.H4('Data Visualization: DFR Onboarding Project'),
    html.P("Select color:"),
    dcc.Dropdown(
        id="dropdown",
        options=['Gold', 'MediumTurquoise', 'LightGreen'],
        value='Gold',
        clearable=False,
    ),html.P("Show Acceleration:"),
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
@app.callback(
    Output("graph", "figure"),
    Input("dropdown", "value"),
    Input("dropdown2", "value"),
    Input("dropdown3", "value"))
def display_color(color, show_accel, show_analog2):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data["timestamp"],
        y=data["Analog Input #2"],
        mode="lines",
        name="Analog Input #2",
        line=dict(color=color),
        visible=show_analog2))

    fig.add_trace(go.Scatter(
        x=data["timestamp"],
        y=data["Accel"],
        mode="lines",
        name="Acceleration",
        visible=show_accel
    ))

    fig.update_layout(
        title="Acceleration vs Time",
        xaxis_title="Time",
        yaxis_title="Value",
        legend_title="Signals"
    )

    return fig

app.run(debug=True)