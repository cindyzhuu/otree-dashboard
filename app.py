# Import required libraries
import dash
from dash import dcc, html, Input, Output, dash_table
import pandas as pd
import plotly.express as px

# Load the data
data = pd.read_excel("OnePager 2021 Q4.xlsx")

# Create the Dash app
app = dash.Dash(__name__)
app.title = "Judiciary One-Pagers"

# Define app layout
app.layout = html.Div([
    html.H1("Judiciary One-Pagers", style={'textAlign': 'center'}),

    # Dropdown for selecting judiciary
    html.Div([
        dcc.Dropdown(
            id='selected_judiciary',
            options=[{'label': name, 'value': name} for name in data['Court_Name'].unique()],
            placeholder="Select a Judiciary"
        )
    ], style={'width': '50%', 'margin': 'auto'}),

    html.H3(id='judiciary_name', style={'textAlign': 'center'}),

    # Row for criminal and civil cases
    html.Div([
        # Criminal column
        html.Div([
            html.H4("Criminal Cases", style={'backgroundColor': '#006400', 'padding': '10px', 'color': 'white'}),
            html.H5("Summary of Key Court Events", style={'backgroundColor': '#9CAF88', 'padding': '10px', 'color': 'white'}),
            dash_table.DataTable(id='criminal_table'),

            html.H5("Case Clearance Rate (CCR)", style={'backgroundColor': '#9CAF88', 'padding': '10px', 'color': 'white'}),
            dcc.Graph(id='ccr_criminal_graph'),

            html.H5("Top Three Reasons for Adjournments", style={'backgroundColor': '#9CAF88', 'padding': '10px', 'color': 'white'}),
            dash_table.DataTable(id='criminal_adjournments')
        ], style={'width': '45%', 'display': 'inline-block', 'verticalAlign': 'top'}),

        # Civil column
        html.Div([
            html.H4("Civil Cases", style={'backgroundColor': '#006400', 'padding': '10px', 'color': 'white'}),
            html.H5("Summary of Key Court Events", style={'backgroundColor': '#9CAF88', 'padding': '10px', 'color': 'white'}),
            dash_table.DataTable(id='civil_table'),

            html.H5("Case Clearance Rate (CCR)", style={'backgroundColor': '#9CAF88', 'padding': '10px', 'color': 'white'}),
            dcc.Graph(id='ccr_civil_graph'),

            html.H5("Top Three Reasons for Adjournments", style={'backgroundColor': '#9CAF88', 'padding': '10px', 'color': 'white'}),
            dash_table.DataTable(id='civil_adjournments')
        ], style={'width': '45%', 'display': 'inline-block', 'verticalAlign': 'top'})
    ])
])

# Define callback for updating judiciary name and tables
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
        return "", [], [], [], [], {}, {}

    filtered_data = data[data['Court_Name'] == selected_judiciary]

    # Create tables
    criminal_table_data = [
        {"Variable": "Criminal Cases Filed", "Value": filtered_data['num_filed_Criminal'].values[0]},
        {"Variable": "Criminal Cases Resolved", "Value": filtered_data['num_resolved_Criminal'].values[0]},
        {"Variable": "Criminal Rulings & Judgments", "Value": filtered_data['num_rul_judg_Criminal'].values[0]},
        {"Variable": "Criminal Adjournments", "Value": filtered_data['num_adj_Criminal'].values[0]}
    ]

    civil_table_data = [
        {"Variable": "Civil Cases Filed", "Value": filtered_data['num_filed_Civil'].values[0]},
        {"Variable": "Civil Cases Resolved", "Value": filtered_data['num_resolved_Civil'].values[0]},
        {"Variable": "Civil Rulings & Judgments", "Value": filtered_data['num_rul_judg_Civil'].values[0]},
        {"Variable": "Civil Adjournments", "Value": filtered_data['num_adj_Civil'].values[0]}
    ]

    # Create adjournments tables
    criminal_adj_data = [
        {"Rank": 1, "Reason": filtered_data['Adj_Criminal_Top_1_Name'].values[0], "Number": 0, "Percent": 0},
        {"Rank": 2, "Reason": filtered_data['Adj_Criminal_Top_2_Name'].values[0], "Number": 0, "Percent": 0},
        {"Rank": 3, "Reason": filtered_data['Adj_Criminal_Top_3_Name'].values[0], "Number": 0, "Percent": 0}
    ]

    civil_adj_data = [
        {"Rank": 1, "Reason": filtered_data['Adj_Civil_Top_1_Name'].values[0], "Number": 0, "Percent": 0},
        {"Rank": 2, "Reason": filtered_data['Adj_Civil_Top_2_Name'].values[0], "Number": 0, "Percent": 0},
        {"Rank": 3, "Reason": filtered_data['Adj_Civil_Top_3_Name'].values[0], "Number": 0, "Percent": 0}
    ]

    # Create CCR graphs
    ccr_periods = ["M1", "M2", "M3"]

    ccr_criminal_fig = px.bar(
        x=ccr_periods,
        y=[filtered_data['CCR_Criminal'].values[0], filtered_data['CCR_Criminal_L1'].values[0], filtered_data['CCR_Criminal_L2'].values[0]],
        labels={'x': 'Period', 'y': 'CCR (%)'},
        title='Criminal Case Clearance Rate (CCR)'
    )

    ccr_civil_fig = px.bar(
        x=ccr_periods,
        y=[filtered_data['CCR_Civil'].values[0], filtered_data['CCR_Civil_L1'].values[0], filtered_data['CCR_Civil_L2'].values[0]],
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

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)