import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import pandas as pd
import sqlite3
import pandas_datareader.data as web
from sqlalchemy import create_engine
import mysql.connector


import p_analatics as p_analytics
import analatics as analytics


from test_api import get_code


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


sidebar_data = get_code("http://127.0.0.1:5000/pages")
print(555555555555555555555555555555555555555555555555555555)
import json
sidebar_data = json.loads(sidebar_data)
sidebar_data = sidebar_data[0].get('code_block')
sidebar = eval(sidebar_data)
# Define the horizontal navbar layout
horizontal_navbar = html.Div(
    className="navbar",
    style={'padding': '20px 0', 'background-color': '#F2F3F8', 'height': '5rem', 'marginBottom': '3rem'},
    children=[
        html.Div(
            className="container",
            children=[
                html.Div(
                    className="row align-items-center",
                    children=[
                        html.Div(
                            className="col",
                            children=[
                                html.Span("From Date", className="font-weight-bold", style={'margin-left': '6rem', 'margin-top': '-2rem'}),
                                dcc.Dropdown(
                                    id='month-dropdown-1',
                                    options=[{'label': month, 'value': month} for month in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']],
                                    value='January',
                                    className='dropdown-style',
                                    style={'width': '150px', 'margin-left': '6rem', 'margin-top': '-2rem'}
                                ),
                            ]
                        ),
                        html.Div(
                            className="col",
                            children=[
                                html.Span("ToDate", className="font-weight-bold", style={'margin-left': '6rem', 'margin-top': '-2rem'}),
                                dcc.Dropdown(
                                    id='month-dropdown-2',
                                    options=[{'label': month, 'value': month} for month in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']],
                                    value='January',
                                    className='dropdown-style',
                                    style={'width': '150px', 'margin-left': '5rem', 'margin-top': '-2rem'}
                                ),
                            ]
                        ),
                        html.Div(
                            className="col", style={'flex': '1'},
                            children=[
                                html.Div(
                                    className="search",
                                    children=[
                                        dcc.Input(
                                            className="form-control mr-sm-2",
                                            type="search",
                                            placeholder="Search Courses",
                                            name="search",
                                            style={'width': '300px', 'height': '35px', 'border-radius': '25px', 'border': 'none', 'margin-left': '6rem', 'margin-top': '-0.8rem'}
                                        ),
                                    ]
                                ),
                            ]
                        ),
                        html.Div(
                            className="col",
                            children=[
                                html.Div(
                                    className="dropdown",
                                    children=[
                                        html.A(
                                            className="nav-link dropdown-toggle",
                                            href="#",
                                            id="navbarDropdownMenuLink",
                                            role="button",
                                            **{"data-toggle": "dropdown", "aria-haspopup": "true", "aria-expanded": "false"},
                                            children=[
                                                html.Img(src="https://s3.eu-central-1.amazonaws.com/bootstrapbaymisc/blog/24_days_bootstrap/fox.jpg", width="40", height="40", className="rounded-circle")
                                            ]
                                        ),
                                        html.Div(
                                            className="dropdown-menu dropdown-menu-end",
                                            style={'width': '150px', 'margin-left': '1rem'},
                                            **{"aria-labelledby": "navbarDropdownMenuLink"},
                                            children=[
                                                html.A(className="dropdown-item", href="#", children="Dashboard"),
                                                html.A(className="dropdown-item", href="#", children="Edit Profile"),
                                                html.A(className="dropdown-item", href="#", children="Log Out")
                                            ]
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ],
    id="navbar-container"
)


content = p_analytics.content

# Landing page layout
landing_page_layout = html.Div(
    [
        html.H1("Welcome to My Dashboard"),
        html.P("This is a simple landing page for the dashboard."),
        html.P("Please use the sidebar navigation to explore the dashboard features."),
        html.Div([
            dcc.Dropdown(['NYC', 'MTL', 'SF'], 'NYC', id='demo-dropdown'),
            html.Div(id='dd-output-container')
        ], className="test_drop")
    ],
    style={'textAlign': 'center', 'padding': '50px'}
)

# App layout
app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    html.Div(horizontal_navbar),
    html.Div(content),
])

# Callback to toggle collapse on sub-menu items
@app.callback(
    [Output("collapse-projects", "is_open"), Output("collapse-team", "is_open")],
    [Input("toggle-projects", "n_clicks"), Input("toggle-team", "n_clicks")],
    [State("collapse-projects", "is_open"), State("collapse-team", "is_open")],
)
def toggle_collapses(n1, n2, is_open1, is_open2):
    if not n1 and not n2:
        return False, False  # Neither button has ever been clicked
    ctx = dash.callback_context
    if not ctx.triggered:
        return False, False  # No clicks yet
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if button_id == "toggle-projects":
        return not is_open1, False
    elif button_id == "toggle-team":
        return False, not is_open2
    return False, False


# Define a callback to update the content of each card
@app.callback(
    [Output(f'card-content-{i}', 'children') for i in range(p_analytics.num_cards)],
    [Input('url', 'pathname')]
)
def update_card_content(pathname):
    # You can add your logic here to update the content based on the pathname
    # For demonstration purposes, I'll just return some sample content
    content = [
        html.P(f"This is card {i+1} content") for i in range(p_analytics.num_cards)
    ]
    return content

# Define a callback to switch between landing page and dashboard
@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def display_page(pathname):
    if pathname == "/":
        return landing_page_layout
    else:
        return content

# Callback to toggle navbar visibility
@app.callback(
    Output("navbar-container", "style"),
    [Input("url", "pathname")]
)
def toggle_navbar_visibility(pathname):
    if pathname == "/":
        return {'display': 'none'}  # Hide the navbar if pathname is '/'
    else:
        return {}  # Show the navbar for other paths




@app.callback(
    Output("query-modal", "is_open"),
    [Input("edit-query-button", "n_clicks"), Input("close-query-button", "n_clicks")],
    [State("query-modal", "is_open")],
)
def toggle_modal(edit_clicks, close_clicks, is_open):
    ctx = dash.callback_context
    if ctx.triggered:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if button_id == "edit-query-button":
            return True
        elif button_id == "close-query-button" and close_clicks:
            return False
    return is_open


@app.callback(
    [Output("ag-grid-table", "rowData"),
     Output("ag-grid-table", "columnDefs")],
    Input("submit-query-button", "n_clicks"),
    State("query-textarea", "value"),
    prevent_initial_call=True
)
def update_ag_grid_on_submit(n_clicks, new_query):
    if n_clicks and new_query:
        print(new_query)  # Print the new query to the console
        df = p_analytics.update_ag_grid(new_query)
        print(df.head())
        row_data = df.to_dict("records")
        column_defs = [{'field': col, 'sortable': True} for col in df.columns]
        return row_data, column_defs
    return dash.no_update, dash.no_update



@app.callback(
    Output("collapse-join", "is_open"),
    Output("card-table", "style"),
    [Input("join-button", "n_clicks")],
    [State("collapse-join", "is_open")]
)
def toggle_collapse(n, is_open):
    if n:
        is_open = not is_open
        card_height = {"width": "80%", "height": "600px"}  # Adjusted height when open
    else:
        is_open = False
        card_height = {"width": "80%", "height": "400px"}  # Initial height when closed

    return is_open, card_height


if __name__ == '__main__':
    app.run_server(debug=True)




    
if __name__ == "__main__":
    app.run_server(debug=True, port=9999)
