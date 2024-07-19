
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
