# Housing Affordability Dashboard in U.S. Cities

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash import Input, Output
import os

# Load dataset (for demonstration purposes, using a CSV file)
csv_file = 'housing_affordability.csv'

data = pd.read_csv(csv_file)

# Calculate the affordability index (Income-to-Housing Cost Ratio)
data['Affordability_Index'] = data['Median_Income'] / data['Median_Home_Price']

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the dashboard with 5 panels (removed the map due to visualization issues)
tabs_styles = {
    'height': '50px'
}
tab_style = {
    'borderBottom': '2px solid #d6d6d6',
    'padding': '15px',
    'fontWeight': 'bold',
    'fontSize': '18px'
}
tab_selected_style = {
    'borderTop': '2px solid #0074D9',
    'borderBottom': '2px solid #0074D9',
    'backgroundColor': '#e6f2ff',
    'color': '#0074D9',
    'padding': '15px'
}

app.layout = html.Div([
    html.H1("Housing Affordability Dashboard", style={'text-align': 'center', 'color': '#2A2A2A', 'margin-bottom': '20px'}),

    # Tabs for 5 different panels
    dcc.Tabs(id='tabs', value='tab1', children=[
        dcc.Tab(label='Affordability Index Overview', value='tab1', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Income vs Home Prices', value='tab2', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Cost of Living Analysis', value='tab3', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Top Affordable Cities', value='tab4', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Least Affordable Cities', value='tab5', style=tab_style, selected_style=tab_selected_style),
    ], style=tabs_styles),

    html.Div(id='tabs-content', style={'margin-top': '20px'})
])

# Callback for updating content based on the selected tab
@app.callback(
    Output('tabs-content', 'children'),
    [Input('tabs', 'value')]
)
def render_content(tab):
    if tab == 'tab1':
        return html.Div([
            html.H3("Affordability Index Across Cities", style={'text-align': 'center'}),
            dcc.Graph(
                figure={
                    'data': [
                        {
                            'x': data['City'],
                            'y': data['Affordability_Index'],
                            'type': 'bar',
                            'marker': {'color': '#1f77b4'}
                        },
                    ],
                    'layout': {
                        'title': 'Affordability Index Across Major U.S. Cities',
                        'xaxis': {'title': 'City'},
                        'yaxis': {'title': 'Affordability Index'},
                        'paper_bgcolor': '#f9f9f9',
                        'plot_bgcolor': '#f9f9f9',
                        'font': {'size': 14}
                    }
                }
            )
        ])

    elif tab == 'tab2':
        return html.Div([
            html.H3("Median Income vs Median Home Price", style={'text-align': 'center'}),
            dcc.Graph(
                figure=px.scatter(
                    data, x='Median_Home_Price', y='Median_Income', color='City',
                    title='Median Income vs Median Home Price',
                    template='plotly_white',
                    size='Affordability_Index',
                    hover_name='City',
                    labels={'Median_Home_Price': 'Median Home Price (USD)', 'Median_Income': 'Median Income (USD)'},
                    color_continuous_scale=px.colors.sequential.Teal
                ).update_layout(
                    paper_bgcolor='#f9f9f9',
                    plot_bgcolor='#f9f9f9',
                    font={'size': 14}
                )
            )
        ])

    elif tab == 'tab3':
        return html.Div([
            html.H3("Cost of Living Analysis", style={'text-align': 'center'}),
            dcc.Graph(
                figure=px.bar(
                    data, x='City', y='Cost_of_Living_Index',
                    title='Cost of Living Index by City',
                    template='plotly_white',
                    color='Cost_of_Living_Index',
                    color_continuous_scale=px.colors.sequential.Magma
                ).update_layout(
                    paper_bgcolor='#f9f9f9',
                    plot_bgcolor='#f9f9f9',
                    font={'size': 14}
                )
            )
        ])

    elif tab == 'tab4':
        top_cities = data.sort_values(by='Affordability_Index', ascending=False).head(5)
        return html.Div([
            html.H3("Top Affordable Cities", style={'text-align': 'center'}),
            dcc.Graph(
                figure=px.bar(
                    top_cities, x='City', y='Affordability_Index',
                    title='Top 5 Most Affordable Cities',
                    template='plotly_white',
                    color='Affordability_Index',
                    color_continuous_scale=px.colors.sequential.Tealgrn
                ).update_layout(
                    paper_bgcolor='#f9f9f9',
                    plot_bgcolor='#f9f9f9',
                    font={'size': 14}
                )
            )
        ])

    elif tab == 'tab5':
        least_affordable = data.sort_values(by='Affordability_Index').head(5)
        return html.Div([
            html.H3("Least Affordable Cities", style={'text-align': 'center'}),
            dcc.Graph(
                figure=px.bar(
                    least_affordable, x='City', y='Affordability_Index',
                    title='Top 5 Least Affordable Cities',
                    template='plotly_white',
                    color='Affordability_Index',
                    color_continuous_scale=px.colors.sequential.Sunset
                ).update_layout(
                    paper_bgcolor='#f9f9f9',
                    plot_bgcolor='#f9f9f9',
                    font={'size': 14}
                )
            )
        ])

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
