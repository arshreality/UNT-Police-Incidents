import plotly.graph_objs as go
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from datetime import datetime

def Header(name, app):
    title = html.H2(name, style={"margin-top": 5})
    logo = html.Img(
        src=app.get_asset_url("logo.png"), style={"float": "right", "height": 50}
    )

    return dbc.Row([dbc.Col(title, md=9), dbc.Col(logo, md=3)])


def LabeledSelect(label, **kwargs):
    return dbc.FormGroup([dbc.Label(label), dbc.Select(**kwargs)])


# Start the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

train_acc = 0.2
test_acc = 0.3

def update_figures():
    num_inc_df = pd.read_csv('num_inc.csv')
    dates = list(num_inc_df['Date'])
    datetimes = sorted([datetime.strptime(x, '%m/%d/%Y') for x in dates])
    fig = go.Figure(data=go.Scatter(x=datetimes, y=list(num_inc_df['Num']), mode='lines+markers'))
    fig.update_layout(
     title={
        'text': "Daily Incidents",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    xaxis_title="Dates",
    yaxis_title="Number of Incidents",
    font=dict(
        size=14,
        color="black"))

    return fig

def map_figure(df, hover_data, color):
    if color == "blue":
        fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", hover_data=hover_data, color_discrete_sequence=[color], zoom=12, height=300, size = "Number of Emergency Phones")
    else:
        fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", hover_data=hover_data, color_discrete_sequence=[color], zoom=12, height=300)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig

def donut():
    df = pd.read_csv('incidents.csv')
    df = df[df.Distance != -1]
    df = df[df.Distance <= 2]

    labels = ['Night', 'Late Night', 'Morning', 'Afternoon']
    times = list(df['Times'])
    freq = {} 
    for items in times: 
        freq[items] = times.count(items)
    
    values = list(freq.values())

    # Use `hole` to create a donut-like pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    
    return fig
# Card components
cards = [
    dbc.Card(
        [
            html.H2(f"{train_acc*100:.2f}%", className="card-title"),
            html.P("Model Training Accuracy", className="card-text"),
        ],
        body=True,
        color="light",
    ),
    dbc.Card(
        [
            html.H2(f"{test_acc*100:.2f}%", className="card-title"),
            html.P("Model Test Accuracy", className="card-text"),
        ],
        body=True,
        color="dark",
        inverse=True,
    ),
    dbc.Card(
        [
            html.H2("YEET", className="card-title"),
            html.P("Train / Test Split", className="card-text"),
        ],
        body=True,
        color="primary",
        inverse=True,
    ),
]

# Graph components
graphs = [
    [
        dcc.RadioItems(
            id="checklist",
            options=[{"label": x, "value": x} 
                    for x in ["Emergency Phones", "Incidents"]],
            value="Incidents",
            labelStyle={'display': 'inline-block'}
        ),
        dcc.Graph(id="map-figure-id"),
    ],
    [
        LabeledSelect(
            id="select-gam",
            options=[{"label": "col_map[k]", "value": "k"}],
            value=['heelo'],
            label="Visualize GAM",
        ),
        dcc.Graph(figure=update_figures()),
    ],
    dcc.Graph(figure=donut())
]

app.layout = dbc.Container(
    [
        Header("UNT Police Incidents", app),
        html.Hr(),
        dbc.Row([dbc.Col(card) for card in cards]),
        html.Br(),
        dbc.Row([dbc.Col(graph) for graph in graphs]),
    ],
    fluid=False,
)

@app.callback(
    Output("map-figure-id", "figure"), 
    [Input("checklist", "value")])
def update_map(map_type):
    if map_type == "Emergency Phones":
        df = pd.read_csv('emergency_phones.csv')
        hover_data = ["Name", "Number of Emergency Phones"]
        color = "blue"

    elif map_type == "Incidents":
        df = pd.read_csv('incidents.csv')
        df = df[df.Distance != -1]
        df = df[df.Distance <= 2]
        hover_data = ["Case", "Reported"]
        color = "red"
    
    return map_figure(df, hover_data, color)

if __name__ == "__main__":
    app.run_server(debug=True)
