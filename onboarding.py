# DFR Onboarding Project

from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd
import numpy as np

#import the data and drop columns with only one unique value to clean up data
data = pd.read_csv('can_data.csv', on_bad_lines='skip', na_values={"timestamp":np.float64, "Analog Input 1":np.float32,
                                              "Analog Input 2":np.float32, "Analog Input 3":np.float32, "Analog Input 4":np.float32,
                                              "Analog Input 5":np.float32, "Analog Input 6":np.float32, "Analog Input 7":np.float32,
                                              "Analog Input 8":np.float32, "Frequency 1":np.float32, "Frequency 2":np.float32, 
                                              "Frequency 3":np.float32, "Frequency 4":np.float32})

print(data.head(10000))
for each in data.columns:
    data[each] = data[each].dropna()
    print("Unique values in: " + str(data[each].nunique()))
    if data[each].nunique() == 1:
        data = data.drop(columns=[each])
print(data.head(10000))

app = Dash(__name__)


app.layout = html.Div([
    html.H4('Interactive color selection with simple Dash example'),
    html.P("Select color:"),
    dcc.Dropdown(
        id="dropdown",
        options=['Gold', 'MediumTurquoise', 'LightGreen'],
        value='Gold',
        clearable=False,
    ),
    dcc.Graph(id="graph"),
])


@app.callback(
    Output("graph", "figure"),
    Input("dropdown", "value"))
def display_color(color):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data["timestamp"],
        y=data["Analog Input 2"],
        mode="lines",
        name="Analog Input 2",
        line=dict(color=color)
    ))

    fig.add_trace(go.Scatter(
        x=data["timestamp"],
        y=data["Analog Input 1"],
        mode="lines",
        name="Analog Input 1"
    ))

    return fig



app.run(debug=True)