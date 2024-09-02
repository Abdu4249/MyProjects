import pandas as pd
import dash
import dash_table
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64
import os

# Path to the dataset
file_path = 'C:/Users/LENOVO/Desktop/Cyber/NetworkData.xlsx'

# Check if the file exists
if not os.path.exists(file_path):
    raise FileNotFoundError(f"The file at {file_path} was not found.")

# Read the dataset
try:
    df = pd.read_excel(file_path)
except Exception as e:
    raise Exception(f"Error reading the Excel file: {e}")

# Assuming df_final is the same as df for now; replace with actual df_final if different
df_final = df  

# Select only numeric columns for the correlation matrix
df_numeric = df.select_dtypes(include=[float, int])
df_final_numeric = df_final.select_dtypes(include=[float, int])

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Function to convert matplotlib figures to base64 URI
def fig_to_uri(fig):
    out_img = io.BytesIO()
    fig.savefig(out_img, format='png', bbox_inches='tight')
    out_img.seek(0)
    encoded = base64.b64encode(out_img.read()).decode("utf-8")
    return "data:image/png;base64,{}".format(encoded)

# Create heatmap figures
def create_heatmap(data):
    fig, ax = plt.subplots(figsize=(12,10 ))  # Adjusted figure size
    sns.heatmap(data, annot=True, ax=ax)
    return fig

# Preprocess Reputation column
def preprocess_reputation(df):
    reputation_counts = df['Reputation'].value_counts(normalize=True)
    reputation_data = pd.Series({'AVERAGE': reputation_counts['AVERAGE'], 'GOOD': reputation_counts['GOOD']})
    return reputation_data

# Preprocess the reputation data
reputation_data = preprocess_reputation(df)

# Identify malicious activities
malicious_activities = df[~df['Reputation'].isin(['Good', 'Average'])]

# Create the layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Network Data Visualization"), className="mb-2")
    ]),
    dbc.Row([
        dbc.Col([
            html.H2("Data Preview"),
            dash_table.DataTable(
                id='data-table',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.head(10).to_dict('records'),
                page_size=10,
                style_table={'overflowX': 'auto'},
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                },
                style_cell={'textAlign': 'left'}
            )
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.H2("Reputation Distribution (Good vs. Average)"),
            dcc.Graph(
                id='reputation-bar',
                figure=px.bar(reputation_data, orientation='h')
            )
        ]),
        dbc.Col([
            html.H2("Protocol Distribution"),
            dcc.Graph(
                id='protocol-bar',
                figure=px.bar(df['PROTOCOL'].value_counts(normalize=True))
            )
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.H2("Heatmap of df"),
            html.Img(src=fig_to_uri(create_heatmap(df_numeric.corr())))
        ]),
        dbc.Col([
            html.H2("Heatmap of df_final"),
            html.Img(src=fig_to_uri(create_heatmap(df_final_numeric.corr())))
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.H2("Class Imbalance Check"),
            dcc.Graph(
                id='class-imbalance',
                figure=px.bar(df_final['Label'].value_counts())
            )
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.H2("Model Accuracy Comparison"),
            dcc.Graph(
                id='model-comparison',
                figure=go.Figure(data=[
                    go.Bar(name='ANN', x=['ANN'], y=[81]),
                    go.Bar(name='Logistic Regression', x=['Logistic Regression'], y=[78]),
                    go.Bar(name='SVM', x=['SVM'], y=[76]),
                    go.Bar(name='Random Forest', x=['Random Forest'], y=[77])
                ])
            )
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.H2("Malicious Activities"),
            dash_table.DataTable(
                id='malicious-activities-table',
                columns=[{"name": i, "id": i} for i in malicious_activities.columns],
                data=malicious_activities.head(100).to_dict('records'),
                page_size=10,
                style_table={'overflowX': 'auto'},
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                },
                style_cell={'textAlign': 'left'}
            )
        ])
    ])
], fluid=True)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
