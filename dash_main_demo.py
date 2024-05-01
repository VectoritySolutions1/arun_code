import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output
import pandas as pd
from dash_ag_grid import AgGrid
import plotly.express as px

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Load your data
df = pd.read_csv("/Users/vectoritytechnologies/Downloads/Download Data - STOCK_US_XNYS_CSV.csv")

# Column definitions for AG Grid
column_defs = [
    {"checkboxSelection": True, "headerCheckboxSelection": True, "suppressSizeToFit": True},
] + [{"headerName": col, "field": col, "sortable": True, "filter": True} for col in df.columns]

data_table = html.Div(
    [
        AgGrid(
            id="row-selection-checkbox-simple",
            columnDefs=column_defs,
            rowData=df.to_dict("records"),
            columnSize="sizeToFit",
            defaultColDef={"filter": True},
            dashGridOptions={
                "rowSelection": "multiple",
                "pagination": True,
                "paginationPageSize": 20,
                "suppressRowClickSelection": True,
                "animateRows": False
            },
        ),
        html.Br(),html.Br(),html.Br(),
        dcc.Graph(id="line-graph")
    ],
)

sidebar = html.Div(
    [
        html.H2("Navigation", className="display-4"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Profile", href="/profile", active="exact"),
                dbc.NavLink("Saved Articles", href="/saved-articles", active="exact"),
                dbc.NavLink("Articles", href="/articles", active="exact"),
                dbc.NavLink("Institutions", href="/institutions", active="exact"),
                dbc.NavLink("Organizations", href="/organizations", active="exact"),
                dbc.NavLink("Settings", href="/settings", active="exact"),
            ],
            vertical=True,
            pills=True
        ),
        html.Hr(),
    ],
    className="sidebar-custom offcanvas-md offcanvas-start p-3"
)

content = html.Div(id="page-content", className="bg-light flex-fill p-4")

app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=False),
        sidebar,
        content
    ],
    className="container-fluid p-0 d-flex h-100"
)

@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):
    if pathname == "/profile":
        return html.Div("This is the Profile page")
    elif pathname == "/saved-articles":
        return data_table
    elif pathname == "/articles":
        return html.Div("This is the Articles page")
    elif pathname == "/institutions":
        return html.Div("This is the Institutions page")
    elif pathname == "/organizations":
        return html.Div("This is the Organizations page")
    elif pathname == "/settings":
        return html.Div("This is the Settings page")
    return html.Div("Welcome to the main page")

@app.callback(
    Output("line-graph", "figure"),
    Input("row-selection-checkbox-simple", "selectedRows")
)
def update_line_chart(selected_rows):
    if not selected_rows:
        # If no rows are selected, display the entire dataset
        return px.line(df, x='Date', y='Close', title='Close Price Over Time')

    # If rows are selected, display only those rows
    selected_df = pd.DataFrame(selected_rows)
    return px.line(selected_df, x='Date', y='Close', title='Selected Rows Close Price Over Time')

if __name__ == "__main__":
    app.run_server(debug=True, port=3333)
