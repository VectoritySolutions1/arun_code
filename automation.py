
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
    [Output("ag-grid-table", "rowData"),
     Output("ag-grid-table", "columnDefs")],
    [Input("submit-query-button", "n_clicks"),
     Input("submit-filters-button", "n_clicks"),
     Input("join-submit-button", "n_clicks")],
    [State("query-textarea", "value"),
     State("table-dropdown-filter", "value"),
     State("filter-rows-container", "children"),
     State("table-dropdown-join-1", "value"),
     State("table-dropdown-join-2", "value"),
     State("join-operation-dropdown", "value"),
     State("column-dropdown-join-1", "value"),
     State("condition-dropdown-join", "value"),
     State("column-dropdown-join-2", "value")],
    prevent_initial_call=True
)
def update_ag_grid_on_submit(query_n_clicks, filter_n_clicks, join_n_clicks,
                             new_query, selected_table, filter_rows,
                             join_table_1, join_table_2, join_operation,
                             join_column_1, join_condition, join_column_2):
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update, dash.no_update

    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    print(f"Triggered ID: {trigger_id}")

    if trigger_id == "submit-query-button" and new_query:
        print("Query Button Triggered")
        df = p_analytics.update_ag_grid(new_query)
        row_data = df.to_dict("records")
        column_defs = [{'field': col, 'sortable': True} for col in df.columns]
        return row_data, column_defs

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

        return row_data, column_defs

    elif trigger_id == "join-submit-button" and join_table_1 and join_table_2 and join_operation and join_column_1 and join_column_2:
        print("Join Button Triggered")
        query = f"SELECT * FROM {join_table_1} {join_operation} {join_table_2} ON {join_table_1}.{join_column_1} {join_condition} {join_table_2}.{join_column_2}"
        print("Join Button", query)
        df = p_analytics.update_ag_grid(query)
        row_data = df.to_dict("records")
        column_defs = [{'field': col, 'sortable': True} for col in df.columns]

        return row_data, column_defs

    return dash.no_update, dash.no_update



