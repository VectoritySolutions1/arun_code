import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output
import pandas as pd
from dash_ag_grid import AgGrid
import plotly.express as px

# Initialize the Dash app with Bootstrap and suppress callback exceptions for dynamically generated components
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# Load your data from CSV files
df = pd.read_csv("/Users/vectoritytechnologies/Downloads/Download Data - STOCK_US_XNYS_CSV.csv")

# Define column definitions for the AG Grid with checkbox selection
column_defs = [
    
    {"checkboxSelection": True, "headerCheckboxSelection": True, "suppressSizeToFit": True},
] + [{"headerName": col, "field": col, "sortable": True, "filter": True} for col in df.columns]

# Define grid options
grid_options = {
    "domLayout": "autoHeight",
    "rowSelection": "multiple",
    "suppressRowClickSelection": True,
    "paginationPageSize": 20,
    "pagination": True,
   
}

# Define the sidebar layout
sidebar = html.Div(
    [
        html.H2("Navigation", className="display-4"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink([html.I(className="fa-regular fa-user"), " Profile"], href="/profile", active="exact", style={'color': 'white'}),
                dbc.NavLink([html.I(className="fa-regular fa-bookmark"), " Saved Articles"], href="/saved-articles", active="exact", style={'color': 'white'}),
                dbc.NavLink([html.I(className="fa-regular fa-newspaper"), " Articles"], href="/articles", active="exact", style={'color': 'white'}),
                dbc.NavLink([html.I(className="fa-solid fa-archway"), " Institutions"], href="/institutions", active="exact", style={'color': 'white'}),
                dbc.NavLink([html.I(className="fa-solid fa-graduation-cap"), " Organizations"], href="/organizations", active="exact", style={'color': 'white'}),
                dbc.NavLink([html.I(className="fa-solid fa-cog"), " Settings"], href="/settings", active="exact", style={'color': 'white'}),
            ],
            vertical=True,
            pills=True,
            className="mynav"
        ),
        html.Hr(),
    ],
    className="sidebar-custom offcanvas-md offcanvas-start p-3",
)

# Define the content layout
content = html.Div(id="page-content", className="bg-light flex-fill p-4")

# Define the full app layout
app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=False),
        sidebar,
        content
    ],
    className="container-fluid p-0 d-flex h-100"
)

# Callback to toggle the settings collapse
@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def display_page(pathname):
    if pathname == "/saved-articles":
        return html.Div([
            AgGrid(
                id="row-selection-checkbox-simple",
                columnDefs=column_defs,
                rowData=df.to_dict("records"),
                dashGridOptions=grid_options,
                style={'width': '100%', 'height': '500px'}
            ),
            html.Br(),html.Br(),html.Br(),
            dcc.Graph(id="line-graph")
        ])
    elif pathname == "/profile":
        return html.Div("Profile Page Content")
    elif pathname == "/articles":
        return html.Div("Articles Page Content")
    elif pathname == "/institutions":
        return html.Div("Institutions Page Content")
    elif pathname == "/organizations":
        return html.Div("Organizations Page Content")
    elif pathname == "/settings":
        return html.Div("Settings Page Content")
    return "Welcome to the Main Page"

# Callback to update the line graph based on selected rows in the AG Grid
@app.callback(
    Output("line-graph", "figure"),
    [Input("row-selection-checkbox-simple", "selectedRows")]
)
def update_line_chart(selected_rows):
    if not selected_rows:
        return px.line(df, x='Date', y='Close', title='Close Price Over Time')

    selected_df = pd.DataFrame(selected_rows)
    return px.line(selected_df, x='Date', y='Close', title='Close Price Over Time')

if __name__ == "__main__":
    app.run_server(debug=True, port=8051)
