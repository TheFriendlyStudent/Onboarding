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

#Convert speed from km/h to m/s
speed_mps = data["Driven Avg Wheel Speed"] / 3.6

#Compute average timestep
dt = data["timestamp"].diff().dt.total_seconds()
dt_mean = dt.mean()

#Smooth speed
speed_smooth = speed_mps.rolling(window=25, center=True).mean()

#Compute acceleration using centered numerical derivative
accel_raw = np.gradient(speed_smooth, dt_mean)

#Smooth acceleration for readability
data["Accel"] = pd.Series(accel_raw).rolling(window=15, center=True).mean()

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

#produce two graphs plotting two inputs: TPS vs Fuel Open Time and Acceleration vs Time, 
#with a polynomial trendline for the first graph
#runtime code to update the graph based on dropdown selections
@app.callback(
    Output("graph", "figure"),
    Input("dropdown2", "value"),
    Input("dropdown3", "value")
)
def display_color(show_accel, show_analog2):

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=False,
        subplot_titles=("TPS vs Fuel Open Time", "Acceleration")
    )

    # Top chart
    fig.add_trace(
        go.Scatter(
            x=data["TPS"],
            y=data["Fuel Open Time"],
            mode="markers",
            marker=dict(size=5, color="blue"),
            name="TPS vs Fuel Open Time"
        ),
        row=1,
        col=1
    )

    # Calculate linear regression
    x = data["TPS"]
    y = data["Fuel Open Time"]
    
    # Fit a 3rd-degree polynomial (cubic)
    coeffs = np.polyfit(x, y, 3)       # 3 = cubic
    trend_y = np.polyval(coeffs, x)    # evaluate the polynomial at each x

    # Optional: sort x for a smooth line
    sorted_idx = np.argsort(x)

    # Add polynomial trendline
    fig.add_trace(
        go.Scatter(
            x=x.values[sorted_idx],
            y=trend_y[sorted_idx],
            mode="lines",
            line=dict(color="green", width=2),
            name="Polynomial Trendline"   # updated label
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
        title="Acceleration vs Time and TPS vs Fuel Open Time",
        showlegend=True
    )

    # Axis labels
    fig.update_xaxes(title_text="TPS (%)", row=1, col=1)
    fig.update_yaxes(title_text="Fuel Open Time (ms)", row=1, col=1)

    fig.update_xaxes(title_text="Time", row=2, col=1)
    fig.update_yaxes(title_text="Acceleration (m/s²)", row=2, col=1)

    return fig

app.run(debug=True)