import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import pandas as pd
import mysql.connector

# Importing get_code from test_api (not provided in this context)
from test_api import get_code

def conn_db():
    db_config = {
        'user': 'root',
        'password': 'root',
        'host': 'localhost',
        'database': 'playwithcode'
    }
    conn = mysql.connector.connect(**db_config)
    return conn

# Initial query to fetch data from stock1
initial_query = """
SELECT * 
FROM stock1
"""

# Initialize connection and fetch initial data
conn = conn_db()
stock_df = pd.read_sql(initial_query, conn)
conn.close()

# Define column definitions for AgGrid
column_defs = [{'field': col, 'sortable': True} for col in stock_df.columns]

# Function to update AgGrid based on query
def update_ag_grid(query):
    conn = conn_db()
    print("**********************************************************************")
    print("newquery", query)
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Create cards dynamically
def create_card(card_id):
    return dbc.Card(
        dbc.CardBody([
            html.Div(id=f'card-content-{card_id}')
        ]),
        className="card l-bg-cherry",
    )

# Number of cards and row of cards
num_cards = 4
cards_row = dbc.Row(
    [dbc.Col(create_card(i), width=3) for i in range(num_cards)],
    className="mb-4 no-gutters justify-content-center",
    style={'marginTop': '50px'}
)

# Initial AgGrid table
ag_grid_table = dag.AgGrid(
    rowData=stock_df.to_dict("records"),
    columnDefs=column_defs,
    defaultColDef={"filter": True},
    dashGridOptions={"enableAdvancedFilter": True, "pagination": True, "paginationPageSize": 20},
    enableEnterpriseModules=True,
    style={"height": 300, "width": "100%"},
    id="ag-grid-table"
)


# Define card layout with initial data and edit button
join_modal = dbc.Modal([
    dbc.ModalHeader("JOIN Tables"),
    dbc.ModalBody([
        dbc.Row([
            dbc.Col(
                dcc.Dropdown(
                    id='table-dropdown-join-11',
                    options=[{'label': 'Table 1', 'value': 'table1'}, {'label': 'Table 2', 'value': 'table2'}],  # Example options
                    placeholder='Select First Table',
                ),
                width=4
            ),
            dbc.Col(
                dcc.Dropdown(
                    id='table-dropdown-join-22',
                    options=[{'label': 'Table 1', 'value': 'table1'}, {'label': 'Table 2', 'value': 'table2'}],  # Example options
                    placeholder='Select Second Table',
                ),
                width=4
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
                width=4
            )
        ]),
        dbc.Row([
            dbc.Col(
                dcc.Dropdown(
                    id='column-dropdown',
                    options=[{'label': col, 'value': col} for col in stock_df.columns],  # Example options
                    placeholder='Select Column',
                ),
                width=4
            ),
            dbc.Col(
                dcc.Dropdown(
                    id='condition-dropdown',
                    options=[
                        {'label': 'Equals', 'value': '='},
                        {'label': 'Not Equals', 'value': '!='},
                        {'label': 'Greater Than', 'value': '>'},
                        {'label': 'Less Than', 'value': '<'}
                    ],
                    placeholder='Select Condition',
                ),
                width=4
            ),
            dbc.Col(
                dcc.Dropdown(
                    id='column-dropdown-2',
                    options=[{'label': col, 'value': col} for col in stock_df.columns],  # Example options
                    placeholder='Select Column',
                ),
                width=4
            )
        ]),
        dbc.Row([
            dbc.Col(
                dbc.Button("+", id="add-dropdown-button", className="btn btn-primary ml-1"),
                width=1
            )
        ]),
        dbc.Row([
            dbc.Col(
                dbc.Button("Submit", id="join-submit-button", color="primary", className="mt-2"),
                width={"size": 2, "offset": 10}
            )
        ])
    ]),
    dbc.ModalFooter([
        dbc.Button("Close", id="close-join-button", className="ml-auto")
    ]),
], id="join-modal", size="lg")

stock_df_columns = stock_df.columns
# cardtable = html.Div([
cardtable = html.Div([
    dbc.Card(
        [
            dbc.CardHeader(
                html.Div([
                    dbc.Button("Edit Query", id="edit-query-button", color="primary", className="float-right"),
                    dbc.Button("JOIN", id="join-button", color="secondary", className="float-right ml-2"),
                    dbc.Button("Code", id="code-button", color="success", className="float-right ml-2"),
                ])
            ),
            dbc.CardBody([
                dbc.Collapse(
                    [
                        dbc.CardHeader(
                            dbc.Tabs(
                                [
                                    dbc.Tab(label="Filter", tab_id="tab-filter"),
                                    dbc.Tab(label="Join operations", tab_id="tab-join"),
                                ],
                                id="tabs-join",
                                active_tab="tab-filter",
                            )
                        ),
                        dbc.CardBody(id="collapse-join-content"),
                    ],
                    id="collapse-join",
                    is_open=False,
                    style={'width': '100%', 'height': '300px'}  # Adjusted width and height
                ),
                dbc.CardFooter("Card Footer"),  # CardFooter outside the Collapse
                html.Div(ag_grid_table),  # Placeholder for ag_grid_table
            ], className="card-body-overflow"),  # Add custom CSS class
        ],
        id="card-table",
        className="mb-3",
        style={"width": "80%", "max-height": "600px", "overflow": "auto"}  # Set max height and overflow for the card
    ),
    dbc.Modal([
        dbc.ModalHeader("Edit Query"),
        dbc.ModalBody([
            dcc.Textarea(id="query-textarea", value=initial_query, style={'width': '100%', 'height': 200}),
        ]),
        dbc.ModalFooter([
            dbc.Button("Submit", id="submit-query-button", color="primary"),
            dbc.Button("Close", id="close-query-button", className="ml-auto")
        ]),
    ], id="query-modal", size="lg"),
    join_modal  # Placeholder for join_modal
])




# Define the content layout
content = html.Div([
    html.Div([
        cards_row,
        dbc.Row([
            cardtable
        ], className="mb-4 no-gutters justify-content-center", style={'marginTop': '50px'})
    ], style={'overflowY': 'auto', 'height': 'calc(100vh - 60px)', 'marginLeft': '80px','background-color': '#f8f9fa'})
], id="page-content")
