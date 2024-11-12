import dash
from dash import dcc, html, Input, Output, dash_table
import pandas as pd
import plotly.express as px

data = pd.read_excel("OnePager 2021 Q4.xlsx")

app = dash.Dash(__name__)
app.title = "Judiciary One-Pagers"

app.layout = html.Div([
    html.H1("Judiciary One-Pagers", style={'textAlign': 'center'}),

    html.Div([
        dcc.Dropdown(
            id='selected_judiciary',
            options=[{'label': name, 'value': name} for name in data['Court_Name'].unique()],
            placeholder="Select a Judiciary"
        )
    ], style={'width': '50%', 'margin': 'auto'}),

    html.H3(id='judiciary_name', style={'textAlign': 'center'}),

    html.Div([
        html.Div([
            html.H4("Criminal Cases", style={'backgroundColor': '#006400', 'padding': '10px', 'color': 'white'}),
            html.H5("Summary of Key Court Events", style={'backgroundColor': '#9CAF88', 'padding': '10px', 'color': 'white'}),
            dash_table.DataTable(id='criminal_table'),

            html.H5("Case Clearance Rate (CCR)", style={'backgroundColor': '#9CAF88', 'padding': '10px', 'color': 'white'}),
            dcc.Graph(id='ccr_criminal_graph'),

            html.H5("Top Three Reasons for Adjournments", style={'backgroundColor': '#9CAF88', 'padding': '10px', 'color': 'white'}),
            dash_table.DataTable(id='criminal_adjournments')
        ], style={'flex': '1 1 50%', 'marginRight': '10px', 'boxSizing': 'border-box'}),

        html.Div([
            html.H4("Civil Cases", style={'backgroundColor': '#006400', 'padding': '10px', 'color': 'white'}),
            html.H5("Summary of Key Court Events", style={'backgroundColor': '#9CAF88', 'padding': '10px', 'color': 'white'}),
            dash_table.DataTable(id='civil_table'),

            html.H5("Case Clearance Rate (CCR)", style={'backgroundColor': '#9CAF88', 'padding': '10px', 'color': 'white'}),
            dcc.Graph(id='ccr_civil_graph'),

            html.H5("Top Three Reasons for Adjournments", style={'backgroundColor': '#9CAF88', 'padding': '10px', 'color': 'white'}),
            dash_table.DataTable(id='civil_adjournments')
        ], style={'flex': '1 1 50%', 'boxSizing': 'border-box'})
    ], style={
        'display': 'flex',
        'justifyContent': 'space-between',
        'alignItems': 'flex-start',
        'width': '100%'
    })
], style={
    'display': 'flex',
    'flexDirection': 'column',
    'alignItems': 'center',
    'justifyContent': 'center',
    'width': '100%',
    'margin': '0 auto'
})

@app.callback(
    [Output('judiciary_name', 'children'),
     Output('criminal_table', 'data'),
     Output('civil_table', 'data'),
     Output('criminal_adjournments', 'data'),
     Output('civil_adjournments', 'data'),
     Output('ccr_criminal_graph', 'figure'),
     Output('ccr_civil_graph', 'figure')],
    [Input('selected_judiciary', 'value')]
)
def update_judiciary(selected_judiciary):
    if not selected_judiciary:
        return "No selection made", [], [], [], [], {}, {}

    filtered_data = data[data['Court_Name'] == selected_judiciary]

    print("Available columns in filtered data:", filtered_data.columns)

    if filtered_data.empty:
        print("No matching data found for the selected judiciary")
        return "No data available", [], [], [], [], {}, {}

    filtered_row = filtered_data.iloc[0]

    ccr_criminal_values = [
        filtered_row.get('CCR_Criminal', 0),
        filtered_row.get('CCR_Criminal_L1', 0),
        filtered_row.get('CCR_Criminal_L2', 0)
    ]

    ccr_civil_values = [
        filtered_row.get('CCR_Civil', 0),
        filtered_row.get('CCR_Civil_L1', 0),
        filtered_row.get('CCR_Civil_L2', 0)
    ]

    if any(pd.isna(val) for val in ccr_criminal_values + ccr_civil_values):
        print("One or more CCR values are missing")
        return "Missing data", [], [], [], [], {}, {}

    criminal_table_data = [
        {"Variable": "Criminal Cases Filed", "Value": filtered_row.get('num_filed_Criminal', 0)},
        {"Variable": "Criminal Cases Resolved", "Value": filtered_row.get('num_resolved_Criminal', 0)},
        {"Variable": "Criminal Rulings & Judgments", "Value": filtered_row.get('num_rul_judg_Criminal', 0)},
        {"Variable": "Criminal Adjournments", "Value": filtered_row.get('num_adj_Criminal', 0)}
    ]

    civil_table_data = [
        {"Variable": "Civil Cases Filed", "Value": filtered_row.get('num_filed_Civil', 0)},
        {"Variable": "Civil Cases Resolved", "Value": filtered_row.get('num_resolved_Civil', 0)},
        {"Variable": "Civil Rulings & Judgments", "Value": filtered_row.get('num_rul_judg_Civil', 0)},
        {"Variable": "Civil Adjournments", "Value": filtered_row.get('num_adj_Civil', 0)}
    ]

    criminal_adj_data = [
        {"Rank": 1, "Reason": filtered_row.get('Adj_Criminal_Top_1_Name', 'N/A'), "Number": 0, "Percent": 0},
        {"Rank": 2, "Reason": filtered_row.get('Adj_Criminal_Top_2_Name', 'N/A'), "Number": 0, "Percent": 0},
        {"Rank": 3, "Reason": filtered_row.get('Adj_Criminal_Top_3_Name', 'N/A'), "Number": 0, "Percent": 0}
    ]

    civil_adj_data = [
        {"Rank": 1, "Reason": filtered_row.get('Adj_Civil_Top_1_Name', 'N/A'), "Number": 0, "Percent": 0},
        {"Rank": 2, "Reason": filtered_row.get('Adj_Civil_Top_2_Name', 'N/A'), "Number": 0, "Percent": 0},
        {"Rank": 3, "Reason": filtered_row.get('Adj_Civil_Top_3_Name', 'N/A'), "Number": 0, "Percent": 0}
    ]

    ccr_criminal_fig = px.bar(
        x=["M1", "M2", "M3"],
        y=ccr_criminal_values,
        labels={'x': 'Period', 'y': 'CCR (%)'},
        title='Criminal Case Clearance Rate (CCR)'
    )

    ccr_civil_fig = px.bar(
        x=["M1", "M2", "M3"],
        y=ccr_civil_values,
        labels={'x': 'Period', 'y': 'CCR (%)'},
        title='Civil Case Clearance Rate (CCR)'
    )

    return (
        selected_judiciary,
        criminal_table_data,
        civil_table_data,
        criminal_adj_data,
        civil_adj_data,
        ccr_criminal_fig,
        ccr_civil_fig
    )

if __name__ == '__main__':
    app.run_server(debug=True)