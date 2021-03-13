import plotly.graph_objs as go

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

def Header(name, app):
    title = html.H2(name, style={"margin-top": 5})
    logo = html.Img(
        src=app.get_asset_url("dash-logo.png"), style={"float": "right", "height": 50}
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
    fig = go.Figure(data=go.Scatter(x=list(num_inc_df['Date']), y=list(num_inc_df['Num'])))

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
        LabeledSelect(
            id="select-coef",
            options=[{"label": "v", "value": "k"}],
            value=['heelo'],
            label="Filter Features",
        ),
        dcc.Graph(id="graph-coef"),
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
]

app.layout = dbc.Container(
    [
        Header("Dash Heart Disease Prediction with AIX360", app),
        html.Hr(),
        dbc.Row([dbc.Col(card) for card in cards]),
        html.Br(),
        dbc.Row([dbc.Col(graph) for graph in graphs]),
    ],
    fluid=False,
)



if __name__ == "__main__":
    app.run_server(debug=True)
