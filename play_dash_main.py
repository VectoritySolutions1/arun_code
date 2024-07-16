import dash
from dash import html, dcc,dash_table
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

conn = p_analytics.conn_db()


from test_api import get_code


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


def get_tables():
    query = "SELECT table_name AS name FROM information_schema.tables WHERE table_schema = 'playwithcode';"
    df = pd.read_sql(query, conn)
    return [{'label': table, 'value': table} for table in df['name']]

# Function to get columns from a specific table
def get_columns(table_name):
    query = f"SELECT column_name AS name FROM information_schema.columns WHERE table_name = '{table_name}' AND table_schema = 'playwithcode';"
    df = pd.read_sql(query, conn)
    return [{'label': col, 'value': col} for col in df['name']]


sidebar_data = get_code("http://127.0.0.1:5000/pages")
print(555555555555555555555555555555555555555555555555555555)
import json
sidebar_data = json.loads(sidebar_data)
sidebar_data = sidebar_data[0].get('code_block')
sidebar = eval(sidebar_data)
# Define the horizontal navbar layout
horizontal_navbar = html.Div(
    className="navbar",
    style={'padding': '20px 0', 'background-color': '#', 'height': '5rem', 'marginBottom': '3rem'},
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
    id="navbar-container",
  
)


playground_content = p_analytics.content
analytics_content = analytics.content



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

content = landing_page_layout

# App layout
app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    html.Div(horizontal_navbar),
    html.Div(analytics_content),
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
    elif pathname == '/analytics':
        return analytics_content
    elif pathname == '/playground/analtics':
        return playground_content
    else:
        return html.Div([html.P("updating.......soon")])

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

# Callback to update ag-grid-table based on filter tab submission
@app.callback(
    [Output("ag-grid-table", "rowData"),
     Output("ag-grid-table", "columnDefs")],
    [Input("submit-filters-button", "n_clicks")],
    [State("table-dropdown-filter", "value"),
     State({"type": "column-dropdown-filter", "index": ALL}, "value"),
     State({"type": "condition-dropdown-filter", "index": ALL}, "value"),
     State({"type": "value-input-filter", "index": ALL}, "value")],
    prevent_initial_call=True
)
def update_ag_grid_on_submit(filters_clicks, selected_table, columns, conditions, values):
    if not all([filters_clicks, selected_table, columns, conditions, values]):
        return dash.no_update, dash.no_update

    # Generate SQL query
    where_clauses = []
    for col, cond, val in zip(columns, conditions, values):
        if col and cond and val:
            where_clauses.append(f"{col} {cond} '{val}'")
    
    where_clause = " AND ".join(where_clauses)
    query = f"SELECT * FROM {selected_table} WHERE {where_clause};"

    # Run the query and fetch results from the database
    df = pd.read_sql(query, conn)
    row_data = df.to_dict("records")
    column_defs = [{'field': col, 'sortable': True} for col in df.columns]
    return row_data, column_defs


# @app.callback(
#     [Output("ag-grid-table", "rowData"),
#      Output("ag-grid-table", "columnDefs")],
#     [Input("submit-filters-button", "n_clicks"),
#      Input("join-submit-button", "n_clicks")],
#     [State("table-dropdown-filter", "value"),
#      State({"type": "column-dropdown-filter", "index": ALL}, "value"),
#      State({"type": "condition-dropdown-filter", "index": ALL}, "value"),
#      State({"type": "value-input-filter", "index": ALL}, "value"),
#      State("table-dropdown-join-1", "value"),
#      State("table-dropdown-join-2", "value"),
#      State("join-operation-dropdown", "value"),
#      State("column-dropdown-join-1", "value"),
#      State("column-dropdown-join-2", "value"),
#      State("condition-dropdown-join", "value")],
#     prevent_initial_call=True
# )
# def update_ag_grid_table(filters_clicks, join_clicks, selected_table_filter, columns_filter, conditions_filter, values_filter,
#                          table_join1, table_join2, join_type, column_join1, column_join2, condition_join):
#     ctx = dash.callback_context

#     if not ctx.triggered:
#         raise dash.exceptions.PreventUpdate
    
#     print("*********************")

#     triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

#     if triggered_id == "submit-filters-button" and filters_clicks:
#         if not all([selected_table_filter, columns_filter, conditions_filter, values_filter]):
#             return dash.no_update, dash.no_update

#         # Generate SQL query for filters
#         where_clauses = []
#         for col, cond, val in zip(columns_filter, conditions_filter, values_filter):
#             if col and cond and val:
#                 where_clauses.append(f"{col} {cond} '{val}'")
        
#         where_clause = " AND ".join(where_clauses)
#         query = f"SELECT * FROM {selected_table_filter} WHERE {where_clause};"

#     elif triggered_id == "join-submit-button" and join_clicks:
#         if not all([table_join1, table_join2, join_type, column_join1, column_join2, condition_join]):
#             return dash.no_update, dash.no_update

#         # Generate SQL query for join operation
#         query = f"SELECT * FROM {table_join1} {join_type} {table_join2} ON {table_join1}.{column_join1} {condition_join} {table_join2}.{column_join2};"

#     # Run the query and fetch results from the database
#     df = pd.read_sql(query, conn)
#     row_data = df.to_dict("records")
#     column_defs = [{'field': col, 'sortable': True} for col in df.columns]
#     return row_data, column_defs







    




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

# Callback to add two additional dropdowns when clicking the "+" button
@app.callback(
    Output('additional-dropdowns-container', 'children'),
    Input('add-dropdown-button', 'n_clicks'),
    State('collapse-join', 'is_open'),
    prevent_initial_call=True
)
def add_additional_dropdowns(n_clicks, is_open):
    if not is_open:
        return []  # If collapse is closed, do not add dropdowns
    
    if n_clicks is None:
        return []  # Initial state, no dropdowns added
    
    # Create two new dropdowns
    additional_dropdowns = dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id=f'table-dropdown-join-{n_clicks * 2 + 1}',
                options=[{'label': 'Table 1', 'value': 'table1'}, {'label': 'Table 2', 'value': 'table2'}],
                placeholder=f'Select First Table {n_clicks * 2 + 1}',
            ),
            width=3
        ),
        dbc.Col(
            dcc.Dropdown(
                id=f'table-dropdown-join-{n_clicks * 2 + 2}',
                options=[{'label': 'Table 1', 'value': 'table1'}, {'label': 'Table 2', 'value': 'table2'}],
                placeholder=f'Select Second Table {n_clicks * 2 + 2}',
            ),
            width=3
        )
    ], className="mt-2")

    return [additional_dropdowns]


@app.callback(
    Output("collapse-join", "style"),
    Input("join-button", "n_clicks"),
    prevent_initial_call=True
)
def toggle_collapse_width(n_clicks):
    if n_clicks is None or n_clicks % 2 == 0:
        return {'width': '0%'}  # Collapse closed or even clicks, set width to 0%
    else:
        return {'width': '100%'}  # Odd clicks, expand width to 100%
    




@app.callback(
    Output("collapse-join-content", "children"),
    [Input("tabs-join", "active_tab")]
)
def render_tab_content(active_tab):
    if active_tab == "tab-filter":
        return dbc.CardBody([
            dbc.Row([
                dbc.Col(
                    dcc.Dropdown(
                        id='table-dropdown-filter',
                        options=get_tables(),  # Populate tables dynamically
                        placeholder='Select Table',
                    ),
                    width=6
                ),
                dbc.Col(
                    dbc.Button("+ Add Filter", id="add-filter-button-filter", color="warning", className="ml-2"),
                    width=2
                )
            ]),
            html.Div(id='filter-rows-container'),  # Container for dynamically added filter rows
            dbc.Row([
                dbc.Col(
                    dbc.Button("Submit Filters", id="submit-filters-button", color="primary", className="mt-3"),
                    width={"size": 2, "offset": 10}
                )
            ]),
        ])
    elif active_tab == "tab-join":
        return dbc.CardBody([
            dbc.Row([
                dbc.Col(
                    dcc.Dropdown(
                        id='table-dropdown-join-1',
                        options=get_tables(),  # Populate tables dynamically
                        placeholder='Select First Table',
                    ),
                    width=3
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='table-dropdown-join-2',
                        options=get_tables(),  # Populate tables dynamically
                        placeholder='Select Second Table',
                    ),
                    width=3
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='join-operation-dropdown',
                        options=[
                            {'label': 'INNER JOIN', 'value': 'INNER JOIN'},
                            {'label': 'LEFT JOIN', 'value': 'LEFT JOIN'},
                            {'label': 'RIGHT JOIN', 'value': 'RIGHT JOIN'},
                            {'label': 'FULL JOIN', 'value': 'FULL JOIN'}
                        ],
                        placeholder='Select Join Operation',
                    ),
                    width=3
                ),
                dbc.Col(
                    dbc.Button("+ Add Condition", id="add-condition-button", color="info", className="ml-2"),
                    width={"size": 2}
                ),
            ]),
            dbc.Row([
                dbc.Col(
                    dcc.Dropdown(
                        id='column-dropdown-join-1',
                        placeholder='Select Column',
                    ),
                    width=3
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='condition-dropdown-join',
                        options=[
                            {'label': 'Equals', 'value': '='},
                            {'label': 'Not Equals', 'value': '!='},
                            {'label': 'Greater Than', 'value': '>'},
                            {'label': 'Less Than', 'value': '<'}
                        ],
                        placeholder='Select Condition',
                    ),
                    width=3
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='column-dropdown-join-2',
                        placeholder='Select Column',
                    ),
                    width=3
                ),
                dbc.Col(
                    dbc.Button("+ Add Filter", id="add-filter-button", color="warning", className="ml-2"),
                    width={"size": 2}
                )
            ]),
            dbc.Row(id='additional-dropdowns-container'),  # Container for additional dropdown rows
            dbc.Row([
                dbc.Col(
                    dbc.Button("Submit", id="join-submit-button", color="primary", className="mt-2"),
                    width={"size": 2, "offset": 10}
                )
            ]),
        ])

@app.callback(
    Output("column-dropdown-filter", "options"),
    [Input("table-dropdown-filter", "value")]
)
def set_columns_dropdown(selected_table):
    if selected_table:
        return get_columns(selected_table)
    return []

@app.callback(
    Output("column-dropdown-join-1", "options"),
    [Input("table-dropdown-join-1", "value")]
)
def set_columns_dropdown_join1(selected_table):
    if selected_table:
        return get_columns(selected_table)
    return []

@app.callback(
    Output("column-dropdown-join-2", "options"),
    [Input("table-dropdown-join-2", "value")]
)
def set_columns_dropdown_join2(selected_table):
    if selected_table:
        return get_columns(selected_table)
    return []

# Callback to manage filter rows dynamically (filter tab)
@app.callback(
    Output("filter-rows-container", "children"),
    [Input("add-filter-button-filter", "n_clicks")],
    [State("filter-rows-container", "children"),
     State("table-dropdown-filter", "value")]
)
def manage_filter_rows(add_clicks, existing_rows, selected_table):
    if existing_rows is None:
        existing_rows = []

    if add_clicks:
        new_row_index = len(existing_rows) + 1
        columns = get_columns(selected_table) if selected_table else []
        new_row = dbc.Row([
            dbc.Col(
                dcc.Dropdown(
                    id={"type": "column-dropdown-filter", "index": new_row_index},
                    options=columns,
                    placeholder='Select Column',
                ),
                width=4
            ),
            dbc.Col(
                dcc.Dropdown(
                    id={"type": "condition-dropdown-filter", "index": new_row_index},
                    options=[
                        {'label': 'Equals', 'value': '='},
                        {'label': 'Not Equals', 'value': '!='},
                        {'label': 'Greater Than', 'value': '>'},
                        {'label': 'Less Than', 'value': '<'}
                    ],
                    placeholder='Select Condition',
                ),
                width=3
            ),
            dbc.Col(
                dcc.Input(
                    id={"type": "value-input-filter", "index": new_row_index},
                    type='text',
                    placeholder='Enter Value',
                ),
                width=3
            ),
            dbc.Col(
                dbc.Button("x", id={"type": "remove-filter-button-filter", "index": new_row_index}, color="danger", className="ml-2"),
                width=1
            )
        ], id={"type": "filter-row", "index": new_row_index})

        existing_rows.append(new_row)

    return existing_rows


# @app.callback(
#     Output("page-content", "children"),
#     [Input("url", "pathname")]
# )
# def display_page(pathname):
#     if pathname == "/":
#         return  landing_page_layout
#     # elif pathname == "/analytics":
#     #     return analytics_page_content()
#     # elif pathname == "/playground":
#     #     return playground_content()
#     else:
#         return html.Div([
#             html.H1("404 - Page not found"),
#             html.P(f"The requested URL {pathname} was not found on this server.")
#         ])




    
if __name__ == "__main__":
    app.run_server(debug=True, port=9999)
