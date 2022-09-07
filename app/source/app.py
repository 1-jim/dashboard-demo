import pandas as pd
import plotly_express as px
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import flask
from datetime import datetime
import SourceIngest as SOURCE

server = flask.Flask(__name__)
app = dash.Dash(
    __name__, server=server,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)
app.config.suppress_callback_exceptions = True

app.title = 'DASHBOARD DEMO'
_version = '0.1 DEMO'
_pageTitle = 'Birdstrikes Data'
_pageSubTitle = app.title
_visDescription = '* WORK IN PROGRESS *'
# Tabs items to visualise from the datasource - testing with vega airports
_chartCollection = ['Species', 'States']

headerImage = 'https://www.google.com/logos/doodles/2022/get-vaccinated-wear-a-mask-save-lives-february-11-12-6753651837109782-2xa.gif'
headerImageAlt = 'Dashboard Logo'

pd.set_option('display.precision', 3)
pd.set_option('display.max_rows', 25)

_activeTabName = "Species"
_tabs = []
for chart in _chartCollection:
    _tabs.append(dbc.Tab(label=chart, tab_id=chart))

app.layout = html.Div(
    children=[
        dbc.Container([
            dcc.Store(id="store"),
            html.Div(className="row"),
            html.Img(alt=headerImageAlt, src=headerImage, height="100em"),
            html.P(_visDescription + str(datetime.now().year),
                   className="lead"),
            html.H2(_pageTitle, className="display-3"),
            html.Hr(),
            html.Div(
                className="Container",
                children=[
                    dbc.Tabs(
                        _tabs,
                        id="tabs",
                        active_tab=_activeTabName
                    )
                ]
            ),
            dcc.Loading(
                id="loading-tabbedgraphcontent",
                type="default",
                color="#f8ca0a",
                fullscreen=False,
                children=[
                    html.Div(id="tab-content", className="p-4"),
                    html.Div(className="row"),
                    dcc.Loading(
                        id="loading-buttonrefresh",
                        type="circle",
                        children=[
                            dbc.Button(
                                [dbc.Spinner(size="sm"), " Regenerate Graphs"],
                                color="primary",
                                id="button",
                                className="mb-3"
                            )
                        ]
                    )
                ]
            )
        ],
            fluid=True,
            className="py-3"
        ),
        html.Footer(
            children=[
                html.Div(
                    className="row",
                    children=[
                        html.Hr(className="my-2"),
                        html.P("¯\_(ツ)_/¯ Version: " + _version +
                               " JCR " + str(datetime.now().year))
                    ]
                )
            ]
        )
    ]
)


@app.callback(Output("tab-content", "children"), [Input("tabs", "active_tab"), Input("store", "data")])
def render_tab_content(active_tab, data):
    if active_tab and data is not None:
        print(data)
        df = getData()
        if active_tab == 'Species':
            return dcc.Graph(figure=figSpecies(df), id='Species', style={'height': '700px'})
        if active_tab == 'States':
            return dcc.Graph(figure=figStates(df), id='States', style={'height': '700px'})
    print(active_tab + ' is the selected tab')
    return "no tab selected!"


@app.callback(Output("store", "data"), [Input("button", "n_clicks")])
def generate_graphs(n):
    if not n:
        # generate an empy graph on app load
        return {k: go.Figure(data=[]) for k in _chartCollection}
    df = getData()
    return {
        'Species': figSpecies(df),
        'States': figStates(df)
    }


def figSpecies(df):
    grp = df.groupby(['wildlife__species'], as_index=False)['cost__total_$'].sum()
    fig = px.bar(
        grp,
        x='wildlife__species',
        y='cost__total_$',
        labels={
            '': '',
            'cost__total_$': 'Total USD Cost'
        },
        color='wildlife__species',
        title='Figure 1'
    )
    return (fig)


def figStates(df):
    grp = df.groupby(['origin_state'], as_index=False)['cost__total_$'].sum()
    fig = px.bar(
        grp,
        x='origin_state',
        y='cost__total_$',
        labels={
            '': '',
            'cost__total_$': 'Total USD Cost'
        },
        color='origin_state',
        title='Figure 2'
    )
    return (fig)


def getData():
    df = SOURCE.processSourceData()
    print(df)
    return (df)


if __name__ == '__main__':
    SOURCE.getExternalSource()
    app.run_server()
