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
    style={'padding': '20px 0', 'background-color': '#134B70', 'height': '5rem', 'marginBottom': '3rem'},
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
                ),
            ]
        )
    ],
    id="navbar-container"
)

sub_navbar = html.Div(
    className="sub-navbar",
    style={'background-color': '#508C9B', 'height': '2.5rem', 'width': '100%', 'display': 'flex', 'align-items': 'center'},
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
                                html.Span("Sub Navbar Section", className="font-weight-bold", style={'color': '#ffffff'}),
                            ]
                        ),
                        html.Div(
                            className="col",
                            style={'display': 'flex', 'justify-content': 'flex-end'},
                            children=[
                                html.Div(
                                    className="playground-icon",
                                    children=[
                                        html.A(
                                            href="/playground/analytics",
                                            className="nav-link",
                                            children="PLAYGROUND",
                                            style={'color': '#ffffff', 'text-decoration': 'none'}
                                        ),
                                    ]
                                ),
                                
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)

# chat_bot = html.Div([
#     html.Div(
#         className="tpbot-icon",
#         style={'position': 'fixed', 'bottom': '100px', 'right': '20px', 'z-index': '1000'},
#         children=[
#             html.A(
#                 id='tpbot-link',
#                 href="#",
#                 className="nav-link btn btn-warning",
#                 children=[
#                     html.Img(src="/assets/image.png", height="30px", className="rounded-circle", style={'margin-right': '10px'}),  # Circular Image
#                 ],
#                 style={'color': '#ffffff', 'text-decoration': 'none', 'padding': '10px 15px'}
#             ),
#         ]
#     ),
    
#     # Chat card component
#     dbc.Card(
#         id='chat-card',
#         style={'position': 'fixed', 'bottom': '90px', 'right': '20px', 'width': '300px', 'border': '1px solid #ccc', 'backgroundColor': '#f9f9f9', 'boxShadow': '0 4px 8px rgba(0,0,0,0.1)'},
#         children=[
#             dbc.CardHeader("Chat with TPBot", style={'backgroundColor': '#EF5A6F', 'color': '#fff'}),
#             dbc.CardBody(id='chat-content', style={'overflowY': 'scroll', 'maxHeight': '300px', 'backgroundColor': '#FFF1DB'}),
#             dbc.CardFooter(
#                 dbc.Input(id='user-input', placeholder='Type your message and press Enter', type='text', style={'width': '100%'})
#             )
#         ]
#     ),

  
# ])





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
    html.Div(sub_navbar),
    html.Div(content),
    html.Div(
        id='tpbot-icon',
        style={'position': 'fixed', 'bottom': '90px', 'right': '20px', 'z-index': '1000'},
        children=[
            html.A(
                id='tpbot-link',
                href="#",
                className="nav-link btn btn-warning",
                children=[
                    html.Img(src="/assets/image.png", height="50px", className="rounded-circle", style={'margin-right': '10px'}),  # Circular Image
                ],
                style={'color': '#ffffff', 'text-decoration': 'none', 'padding': '10px 15px'}
            ),
        ]
    ),

    # Chat card component (hidden by default)
      dbc.Card(
        id='chat-card',
        style={'display': 'none', 'position': 'fixed', 'bottom': '20px', 'right': '20px', 'width': '10cm', 'height': '10cm', 'border': '1px solid #ccc', 'backgroundColor': '#f9f9f9', 'boxShadow': '0 4px 8px rgba(0,0,0,0.1)', 'overflow': 'hidden'},
        children=[
            dbc.CardHeader("Chat with TPBot", style={'backgroundColor': '#EF5A6F', 'color': '#fff', 'height': '1cm', 'textAlign': 'center', 'lineHeight': '1cm'}),  # Header color
            dbc.CardBody(
                dbc.ListGroup(id='chat-content', style={'overflowY': 'auto', 'backgroundColor': '#FFF1DB', 'padding': '10px', 'height': '8cm'}),
                style={'height': '8cm', 'backgroundColor': '#FFF1DB'}
            ),  # Body color
            dbc.Input(id='user-input', placeholder='Type your message and press Enter', type='text', style={'width': '100%', 'margin-top': '10px', 'borderRadius': '8px', 'height': '1cm'}),
            dbc.CardFooter(
                dbc.Button("Close", id="close-button", color="secondary", size="sm", className="mr-1"),
                style={'backgroundColor': '#536493', 'color': 'white', 'textAlign': 'center', 'height': '1cm', 'lineHeight': '1cm'}
            )
        ]
    ),
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
    return dbc.CardBody([
        dcc.Tabs(id="tabs-join", value='tab-filter', children=[
            dcc.Tab(label='Filter', value='tab-filter', children=[
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
            ]),
            dcc.Tab(label='Join', value='tab-join', children=[
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
                        dbc.Button("Submit", id="join-submit-button", color="warning", className="mt-2"),
                        width={"size": 2, "offset": 10}
                    )
                ]),
            ])
        ])
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


@app.callback(
    Output("filter-rows-container", "children"),
    [Input("add-filter-button-filter", "n_clicks"),
     Input({"type": "remove-filter-button-filter", "index": ALL}, "n_clicks")],
    [State("filter-rows-container", "children"),
     State("table-dropdown-filter", "value")]
)
def manage_filter_rows(add_clicks, remove_clicks, existing_rows, selected_table):
    ctx = dash.callback_context

    if not existing_rows:
        existing_rows = []

    print("*************THIS ID IS FROM MANAGER FITER********************8")
    value = ctx.triggered[0]['prop_id'].split('.')[0]
    print(value)
    if 'remove-filter-button-filter' in value:
        print("ssssssssssssssssssssssssssssss")


    if ctx.triggered and ctx.triggered[0]['prop_id'] == 'add-filter-button-filter.n_clicks':
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

    elif 'remove-filter-button-filter' in value :
        print("OKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
        print(111111,ctx.triggered[0]['prop_id'].split('.')[0].split('index":')[1].strip('}'))
        remove_index = ctx.triggered[0]['prop_id'].split('.')[0].split('index":')[1].strip('}')
        print(remove_index[0])
        print("exisiting ")
        print(existing_rows)
        existing_rows = [row for row in existing_rows if row['props']['id']['index'] != int(remove_index[0])]

    return existing_rows
@app.callback(
    [Output("ag-grid-table", "rowData"),
     Output("ag-grid-table", "columnDefs"),
     Output('output-div', 'children')],
    [Input("submit-query-button", "n_clicks"),
     Input("submit-filters-button", "n_clicks"),
     Input("join-submit-button", "n_clicks"),
     Input('execute-button', 'n_clicks')],
    [State("query-textarea", "value"),
     State("table-dropdown-filter", "value"),
     State("filter-rows-container", "children"),
     State("table-dropdown-join-1", "value"),
     State("table-dropdown-join-2", "value"),
     State("join-operation-dropdown", "value"),
     State("column-dropdown-join-1", "value"),
     State("condition-dropdown-join", "value"),
     State("column-dropdown-join-2", "value"),
     State('code-editor', 'value')],
    prevent_initial_call=True
)
def update_ag_grid_on_submit(query_n_clicks, filter_n_clicks, join_n_clicks, execute_n_clicks,
                             new_query, selected_table, filter_rows,
                             join_table_1, join_table_2, join_operation,
                             join_column_1, join_condition, join_column_2,
                             code):
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update, dash.no_update, dash.no_update

    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    print(f"Triggered ID: {trigger_id}")

    if trigger_id == "execute-button" and code:
        print('code---->', code)
        try:
            import requests
            response = requests.post('http://127.0.0.1:5000/execute_python', json={'code': code})
            response.raise_for_status()  # Raise an exception for HTTP errors
            result = response.json().get('result', 'No result returned')
            print(type(result))

            # Convert result to DataFrame if needed
            import pandas as pd
            try:
                df = pd.DataFrame(result)  # Adjust based on the result format
                row_data = df.to_dict("records")
                column_defs = [{'field': col, 'sortable': True} for col in df.columns]
                return row_data, column_defs, result
            except Exception as e:
                return dash.no_update, dash.no_update, f'Error converting result to DataFrame: {str(e)}'

        except requests.RequestException as e:
            return dash.no_update, dash.no_update, f'Error: {str(e)}'

    if trigger_id == "submit-query-button" and new_query:
        print("Query Button Triggered")
        df = p_analytics.update_ag_grid(new_query)
        row_data = df.to_dict("records")
        column_defs = [{'field': col, 'sortable': True} for col in df.columns]
        return row_data, column_defs, dash.no_update

    elif trigger_id == "submit-filters-button" and selected_table:
        print("Filters Button Triggered")
        query = f"SELECT * FROM {selected_table} WHERE "
        conditions = []

        for row in filter_rows:
            row_id = row["props"]["id"]["index"]
            column = row["props"]["children"][0]["props"]["children"]["props"]["value"]
            condition = row["props"]["children"][1]["props"]["children"]["props"]["value"]
            value = row["props"]["children"][2]["props"]["children"]["props"]["value"]
            print(f"Row {row_id}: column={column}, condition={condition}, value={value}")

            if column and condition and value:
                conditions.append(f"{column} {condition} '{value}'")

        if conditions:
            query += " AND ".join(conditions)
        else:
            query = f"SELECT * FROM {selected_table}"  # Fallback query

        df = p_analytics.update_ag_grid(query)
        row_data = df.to_dict("records")
        column_defs = [{'field': col, 'sortable': True} for col in df.columns]

        return row_data, column_defs, dash.no_update

    elif trigger_id == "join-submit-button" and join_table_1 and join_table_2 and join_operation and join_column_1 and join_column_2:
        print("Join Button Triggered")
        query = f"SELECT * FROM {join_table_1} {join_operation} {join_table_2} ON {join_table_1}.{join_column_1} {join_condition} {join_table_2}.{join_column_2}"
        print("Join Button", query)
        df = p_analytics.update_ag_grid(query)
        row_data = df.to_dict("records")
        column_defs = [{'field': col, 'sortable': True} for col in df.columns]

        return row_data, column_defs, dash.no_update

    return dash.no_update, dash.no_update, dash.no_update




@app.callback(
    Output("offcanvas", "is_open"),
    Input("code-button", "n_clicks"),
    [State("offcanvas", "is_open")]
)
def toggle_offcanvas(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

# @app.callback(
#     Output('output-div', 'children'),
#     Input('execute-button', 'n_clicks'),
#     State('code-editor', 'value')
# )
# def execute_code(n_clicks, code):
#     import requests
#     if n_clicks:
#         print('code---->', code)
#         try:
#             response = requests.post('http://127.0.0.1:5000/execute_python', json={'code': code})
#             response.raise_for_status()  # Raise an exception for HTTP errors
#             result = response.json().get('result', 'No result returned')
#             print(type(result))
#         except requests.RequestException as e:
#             result = f'Error: {str(e)}'
#         return result
#     return ""



bot_responses = {
    "hi": "Hi, how can I assist you today?",
    "hello": "Hello there! How can I help?",
    "goodbye": "Goodbye! Have a great day!",
    "help": "Sure, I'm here to help. What do you need?",
}

# Callback to toggle the chat card visibility and handle user input
@app.callback(
    Output('chat-card', 'style'),
    [Input('tpbot-link', 'n_clicks')],
    [State('chat-card', 'style')],
    prevent_initial_call=True
)
def toggle_chat_card(n_clicks, chat_card_style):
    if n_clicks is not None and n_clicks % 2 == 1:
        chat_card_style['display'] = 'block'
    else:
        chat_card_style['display'] = 'none'
    return chat_card_style

# Callback to update chat content and handle bot responses
@app.callback(
    Output('chat-content', 'children'),
    [Input('user-input', 'n_submit')],
    [State('user-input', 'value'), State('chat-content', 'children')],
    prevent_initial_call=True
)
def update_chat_content(n_submit, user_input, chat_content):
    if not chat_content:  # Initialize chat_content if it's None or empty
        chat_content = []
    
    if user_input:
        user_message = user_input.lower().strip()
        if user_message in bot_responses:
            bot_message = bot_responses[user_message]
        else:
            bot_message = "I'm sorry, I didn't understand that."
        
        # Add user message
        new_user_message = dbc.ListGroupItem(f"You: {user_input}", color="info", className="mb-1")
        chat_content.append(new_user_message)
        
        # Add bot response
        new_bot_message = dbc.ListGroupItem(f"Bot: {bot_message}", className="mb-1")
        chat_content.append(new_bot_message)
    
    return chat_content







    
if __name__ == "__main__":
    app.run_server(debug=True, port=9999)
