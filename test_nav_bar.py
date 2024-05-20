import dash
from dash import html, dcc
#from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from datetime import datetime
import plotly.express as px
from dash.dependencies import Input, Output, State, MATCH, ALL
import dash_ag_grid as dag
import numpy as np
import pandas as pd
import pandas_datareader.data as web

def fetch_stock_data(symbol, start_date, end_date):
    df = web.DataReader('AAPL', 'av-daily', start='2022-01-01', end='2022-12-31', api_key='your_api_key')
    return df

symbol = 'AAPL'  # Example stock symbol (Apple)
start_date = '2022-01-01'
end_date = '2022-12-31'
stock_df = fetch_stock_data(symbol, start_date, end_date)
# Define the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Sample data for the graphs
# data = px.data.iris()  # Sample dataset

# df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv")
column_defs = [
    {'field': 'Date', 'sortable': True},
    {'field': 'Open', 'sortable': True},
    {'field': 'High', 'sortable': True},
    {'field': 'Low', 'sortable': True},
    {'field': 'Close', 'sortable': True},
    {'field': 'Volume', 'sortable': True},
]

ag_grid_table= dag.AgGrid(
    rowData=stock_df.to_dict("records"),
    columnDefs=[{"field": i} for i in stock_df.columns],
    defaultColDef={"filter": True},
    dashGridOptions={"enableAdvancedFilter": True,"pagination": True,"paginationPageSize": 20},
    enableEnterpriseModules=True,
    style={"height": 300, "width": "100%"},
    
   # licenseKey= enter your license key here
)
card_10_content = html.Div([
    html.H5("Card 10 Title", className="card-title"),
    html.Div(ag_grid_table, style={'height': '300px'})  # Adjust height as needed
])

# Define the card creation function with custom styles
# def create_card():
#     return dbc.Card(
#         dbc.CardBody([
#             html.H4("Card Title", className="card-title"),
#             html.P("This is some card content", className="card-text"),
#         ]),
#         className="card l-bg-cherry",
#         style={'borderRadius': '10px', 'border': 'none', 'position': 'relative', 'marginBottom': '30px', 'boxShadow': '0 0.46875rem 2.1875rem rgba(90,97,105,0.1), 0 0.9375rem 1.40625rem rgba(90,97,105,0.1), 0 0.25rem 0.53125rem rgba(90,97,105,0.12), 0 0.125rem 0.1875rem rgba(90,97,105,0.1)'}
#     )

# # Create a row of cards with only three cards
# cards_row = dbc.Row(
#     [dbc.Col(create_card(), width=4) for _ in range(3)],  # Create 3 columns containing cards
#     className="mb-4 no-gutters",  # Margin bottom for spacing between rows, no gutters
#     style={'marginLeft': '10rem', 'marginRight': '5rem'}  # Add margin on both sides
# )

# Define the card creation function with custom styles
def create_card(card_id):
    return dbc.Card(
        dbc.CardBody([
            html.Div(id=f'card-content-{card_id}')
        ]),
        className="card l-bg-cherry",
        #style={'borderRadius': '10px', 'border': 'none', 'position': 'relative', 'marginBottom': '30px', 'boxShadow': '0 0.46875rem 2.1875rem rgba(90,97,105,0.1), 0 0.9375rem 1.40625rem rgba(90,97,105,0.1), 0 0.25rem 0.53125rem rgba(90,97,105,0.12), 0 0.125rem 0.1875rem rgba(90,97,105,0.1)'}
    )

# Create cards dynamically
num_cards = 4
cards_row = dbc.Row(
    [dbc.Col(create_card(i), width=3) for i in range(num_cards)],  # Create columns containing cards
    className="mb-4 no-gutters justify-content-center",  # Margin bottom for spacing between rows, no gutters
    style={'marginTop': '50px'}  # Add margin on top
)


card_5 = dbc.Card(
    dbc.CardBody([
        html.H5("Card 5 Title", className="card-title"),
        html.P("This is card 5 content", className="card-text"),
    ]),
    className="card card-5",  # Add specific class for card_5
    id='card-5',
    style={'width': '98%', 'height': '250px'}  # Adjust width and height
)

card_6 = dbc.Card(
    dbc.CardBody([
        html.H5("Card 6 Title", className="card-title"),
        html.P("This is card 6 content", className="card-text"),
    ]),
    className="card card-6",  # Add specific class for card_6
    id='card-6',
    style={'width': '97%', 'height': '250px'}  # Adjust width and height
)
card_7 = dbc.Card(
    dbc.CardBody([
        html.H5("Card 7 Title", className="card-title"),
        html.P("This is card 5 content", className="card-text"),
    ]),
    className="card card-5",  # Add specific class for card_5
    id='card-7',
    style={'width': '98%', 'height': '250px'}  # Adjust width and height
)

card_8 = dbc.Card(
    dbc.CardBody([
        html.H5("Card 8 Title", className="card-title"),
        html.P("This is card 5 content", className="card-text"),
    ]),
    className="card card-5",  # Add specific class for card_5
    id='card-8',
    style={'width': '98%', 'height': '250px'}  # Adjust width and height
)

card_9 = dbc.Card(
    dbc.CardBody([
        html.H5("Card 9 Title", className="card-title"),
        html.P("This is card 5 content", className="card-text"),
    ]),
    className="card card-5",  # Add specific class for card_5
    id='card-5',
    style={'width': '98%', 'height': '250px'}  # Adjust width and height
)

card_10 = dbc.Card(
    dbc.CardBody(card_10_content),
    className="card card-5",
    id='card-10',
    style={'width': '98%', 'height': '400px'}  # Adjust width and height
)


# Callback to update the content of each card
@app.callback(
    [Output(f'card-content-{i}', 'children') for i in range(num_cards)],
    [Input('url', 'pathname')]
)
def update_card_content(pathname):
    # You can add your logic here to update the content based on the pathname
    # For demonstration purposes, I'll just return some sample content
    content = [
        html.P(f"This is card {i+1} content") for i in range(num_cards)
    ]
    return content

# Define the sidebar layout with collapsible sub-menus
sidebar = html.Div([
    html.H2("Bedimcode", className="display-4"),
    html.Hr(),
    dbc.Nav([
        dbc.NavLink([html.I(className="bi bi-bar-chart-line-fill"), html.Span("Dashboard")], href="/", active="exact", className="nav-link"),
        dbc.NavLink([html.I(className="bi bi-bar-chart-line-fill"), html.Span("Messenger")], href="/messenger", active="exact", className="nav-link"),
        dbc.NavLink("Analytics", href="/analytics", active="exact", className="nav-link"),
        dbc.NavLink("Settings", href="/settings", active="exact", className="nav-link"),
        dbc.NavItem([
            dbc.NavLink("Projects", href="#", className="nav-link", id="toggle-projects"),
            dbc.Collapse(
                dbc.Nav([
                    dbc.NavLink("Data", href="/projects/data", className="nav-link"),
                    dbc.NavLink("Group", href="/projects/group", className="nav-link"),
                    dbc.NavLink("Members", href="/projects/members", className="nav-link"),
                ], vertical=True, pills=True),
                id="collapse-projects",
            ),
        ]),
        dbc.NavItem([
            dbc.NavLink("Team", href="#", className="nav-link", id="toggle-team"),
            dbc.Collapse(
                dbc.Nav([
                    dbc.NavLink("Data", href="/team/data", className="nav-link"),
                    dbc.NavLink("Group", href="/team/group", className="nav-link"),
                    dbc.NavLink("Members", href="/team/members", className="nav-link"),
                ], vertical=True, pills=True),
                id="collapse-team",
            ),
        ]),
        dbc.NavLink("Log Out", href="/logout", active="exact", className="nav-link"),
    ], vertical=True, pills=True, className="flex-column"),
], className="sidebar")

# Horizontal Navbar

horizontal_navbar = html.Div(
    className="navbar",
    style={'padding': '20px 0', 'background-color': '#F2F3F8', 'height': '5rem', 'marginBottom': '3rem'},  # Increase padding to increase height and set background color
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
                                    options=[
                                        {'label': month, 'value': month} for month in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
                                    ],
                                    value='January',
                                    className='dropdown-style',
                                    style={'width': '150px', 'margin-left': '6rem', 'margin-top': '-2rem'}  # Set width of the dropdown
                                ),
                            ]
                        ),
                        html.Div(
                            className="col",
                            children=[
                                html.Span("ToDate", className="font-weight-bold", style={'margin-left': '6rem', 'margin-top': '-2rem'}),
                                dcc.Dropdown(
                                    id='month-dropdown-2',
                                    options=[
                                        {'label': month, 'value': month} for month in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
                                    ],
                                    value='January',
                                    className='dropdown-style',
                                    style={'width': '150px', 'margin-left': '5rem', 'margin-top': '-2rem'}  # Set width of the dropdown
                                ),
                            ]
                        ),
                        html.Div(
                            className="col", style={'flex': '1'},  # Set the third column to take up the remaining space
                            children=[
                                html.Div(
                                    className="search",
                                    children=[
                                        dcc.Input(
                                            className="form-control mr-sm-2",
                                            type="search",
                                            placeholder="Search Courses",
                                            name="search",
                                            style={'width': '300px', 'height': '35px', 'border-radius': '25px', 'border': 'none','margin-left': '6rem','margin-top': '-0.8rem'}
                                        ),
                                    ]
                                ),
                            ]
                        ),
                        html.Div(  # Move this div to the end for profile dropdown
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
                                            style={'width': '150px','margin-left':'1rem'},  # Adjust width of the dropdown menu
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
content = html.Div([
    html.Div([
        cards_row,  # Insert the row of cards at the top of the content
        dbc.Row([
           html.Div(card_5, className="col card-wrapper"),
           html.Div(card_6, className="col card-wrapper")
        ], className="mb-4 no-gutters justify-content-center", style={'marginTop': '50px'}),
        dbc.Row([
           html.Div(card_7, className="col card-wrapper"),
           html.Div(card_8, className="col card-wrapper"),
           html.Div(card_9, className="col card-wrapper"),

        ], className="mb-4 no-gutters justify-content-center", style={'marginTop': '50px'}),
        dbc.Row([
           html.Div(card_10, className="col card-wrapper")

        ], className="mb-4 no-gutters justify-content-center", style={'marginTop': '50px'})  # Add margin on top
    ], style={'overflowY': 'auto', 'height': 'calc(100vh - 60px)', 'marginLeft': '80px'})  
], id="page-content")

# Landing page layout
landing_page_layout = html.Div(
    [
        html.H1("Welcome to My Dashboard"),
        html.P("This is a simple landing page for the dashboard."),
        html.P("Please use the sidebar navigation to explore the dashboard features."),
        html.Div([
            dcc.Dropdown(['NYC', 'MTL', 'SF'], 'NYC', id='demo-dropdown'),
            html.Div(id='dd-output-container')
        ],className="test_drop")
    ],
    style={'textAlign': 'center', 'padding': '50px'}
)

# App layout
app.layout = html.Div([
    dcc.Location(id="url"),  # Add the URL component
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
def toggle_collapse(n1, n2, is_open1, is_open2):
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

# Define the callback to switch between landing page and dashboard
@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def display_page(pathname):
    if pathname == "/":
        return landing_page_layout
    else:
        return content


@app.callback(
    Output("navbar-container", "style"),
    [Input("url", "pathname")]
)
def toggle_navbar_visibility(pathname):
    if pathname == "/":
        return {'display': 'none'}  # Hide the navbar if pathname is '/'
    else:
        return {}  # Show the navbar for other paths


from dash.exceptions import PreventUpdate


if __name__ == "__main__":
    app.run_server(debug=True,port=9999)
