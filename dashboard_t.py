import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
from dash_ag_grid import AgGrid

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

df = pd.read_csv("/Users/vectoritytechnologies/Downloads/Download Data - STOCK_US_XNYS_CSV.csv")


df_data = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/ag-grid/olympic-winners.csv"
)



# column_defs = [
#     {"headerName": col, "field": col, "sortable": True, "filter": True} for col in df.columns
# ]

column_defs = [
    {"checkboxSelection": True, "headerCheckboxSelection": True, "suppressSizeToFit": True},
] + [{"headerName": col, "field": col, "sortable": True, "filter": True} for col in df.columns]

grid_options = {
    "domLayout": "autoHeight",
    "rowSelection": "multiple",
    "suppressRowClickSelection": True,
}

data_table = html.Div(
    [
        AgGrid(
            id="row-selection-checkbox-simple",
            columnDefs=column_defs,
            rowData=df.to_dict("records"),
            columnSize="sizeToFit",
            defaultColDef={"filter": True},
            dashGridOptions={"rowSelection": "multiple","pagination": True,
                            "paginationPageSize": 20,"rowSelection": "multiple", "suppressRowClickSelection": True, "animateRows": False},
        ),
           html.Br(),html.Br(),html.Br(),
            dcc.Graph(id="line-graph")
    ],
)


table =AgGrid(
                    id="my_ag_grid",
                        rowData=df.to_dict("records"),
                        columnDefs=[
                            {
                                "field": c,
                                "filter": "agNumberColumnFilter"
                                if c
                                in [
                                    "year",
                                    "primary_energy_consumption",
                                    "renewables_consumption",
                                ]
                                else "agTextColumnFilter",
                                "floatingFilter": True,
                                "resizable": True,
                                "sortable": True,
                                "editable": True,
                            }
                            for c in df.columns
                        ],
                        defaultColDef={
                            "filter": True,
                            "sortable": True,
                        },
                        #dashGridOptions={"rowSelection": "multiple", "suppressRowClickSelection": True, "animateRows": False},
                        dashGridOptions={
                            "pagination": True,
                            "paginationPageSize": 20,
                            "enableFilter": True,
                            "rowSelection": "multiple", 
                            "suppressRowClickSelection": True,
                             "animateRows": False
                        },
                    ),
                  
            

# Define the sidebar layout using the custom CSS class from assets/custom_styles.css
sidebar = html.Div(
    [
        html.H2("Navigation", className="display-4"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink([html.I(className="fa-regular fa-user"), " Profile"], href="/profile", active="exact", style={'color': 'white'}),
                dbc.NavLink([html.I(className="fa-regular fa-bookmark"), " Saved Articles", html.Span("5", className="notification-badge")], href="/saved-articles", active="exact", style={'color': 'white'}),
                dbc.NavLink([html.I(className="fa-regular fa-newspaper"), " Articles"], href="/articles", active="exact", style={'color': 'white'}),
                dbc.NavLink([html.I(className="fa-solid fa-archway"), " Institutions"], href="/institutions", active="exact", style={'color': 'white'}),
                dbc.NavLink([html.I(className="fa-solid fa-graduation-cap"), " Organizations"], href="/organizations", active="exact", style={'color': 'white'}),
                dbc.NavLink(
                    [
                        html.I(className="fas fa-cog pe-2"),
                        " Settings",
                    ],
                    href="/settings",
                    active="exact",
                    className="sidebar-link collapsed",
                    id="settings-collapse",
                    style={'color': 'white'},
                ),
                dbc.Collapse(
                    [
                        dbc.NavLink([html.I(className="fas fa-sign-in-alt pe-2"), " Login"], href="/login", active="exact", className="sidebar-link", style={'color': 'white'}),
                        dbc.NavLink([html.I(className="fas fa-user-plus pe-2"), " Register"], href="/register", active="exact", className="sidebar-link", style={'color': 'white'}),
                        dbc.NavLink([html.I(className="fas fa-sign-out-alt pe-2"), " Log Out"], href="/logout", active="exact", className="sidebar-link", style={'color': 'white'}),
                    ],
                    id="settings-collapse-content",
                ),
            ],
            vertical=True,
            pills=True,
            className="mynav"
        ),
        html.Hr(),
        html.Div(
            [
                html.I(className="fa-solid fa-book me-2"),
                html.Span(
                    [
                        html.H6("Geeks for Geeks Learning Portal", className="mt-1 mb-0", style={'color': 'white'}),
                    ]
                ),
            ],
            className="d-flex"
        ),
    ],
    className="sidebar-custom offcanvas-md offcanvas-start p-3",  # Apply custom CSS class
)

# Define the content layout
content = html.Div(id="page-content", className="bg-light flex-fill p-4")

# Define the app layout
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
    Output("settings-collapse-content", "is_open"),
    [Input("settings-collapse", "n_clicks")],
    [Input("settings-collapse-content", "is_open")],
)
def toggle_settings_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

# Callback to update the content based on the URL
@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def display_page(pathname):
    if pathname == "/profile":
        return html.Div(table)
    elif pathname == "/saved-articles":
        return html.Div(data_table)
    elif pathname == "/articles":
        return html.Div("This is the articles page")
    elif pathname == "/institutions":
        return html.Div("This is the institutions page")
    elif pathname == "/organizations":
        return html.Div("This is the organizations page")
    elif pathname == "/settings":
        return html.Div("This is the settings page")
    elif pathname == "/login":
        return html.Div("This is the login page")
    elif pathname == "/register":
        return html.Div("This is the register page")
    elif pathname == "/logout":
        return html.Div("This is the logout page")
    return html.Div("Welcome to the main page")

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
    app.run_server(debug=True,port=3333)
