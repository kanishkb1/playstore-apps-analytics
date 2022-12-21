#importing necessary libraries
import pandas as pd
import numpy as np
import plotly as pt
import plotly.graph_objects as go
import preprocess
#importing dash associated libraries
import dash #to build interactive layouts
from dash import html#to built interactivity to application
from dash import dcc
from dash import dash_table #to enable the interactive table view
from dash.dependencies import Input, Output

#load the dataset
dataframe = pd.read_csv('playstore_analysis.csv')

dataframe = preprocess.run(dataframe)
#instance of Dash class
app= dash.Dash()

temp = dataframe.groupby('Category').agg( {"Installs":"sum"}).reset_index()
temp.sort_values(by=['Installs'], inplace=True, ascending=False)
temp = temp.head(15)
pieplotfig = go.Figure()
pieplotfig.add_trace(go.Pie(
                    labels=temp.Category,
                    values=temp.Installs,
                    textinfo='label+percent',
                    insidetextorientation='radial',
                    pull = 0.05
  ))
pieplotfig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 40},bargap=0.05, autosize=True)


app.layout = html.Div([
    html.Div([
        html.H3('Data-Centric Dashboard', style={'textAlign': 'center'})],
        style={'width': '100%', 'display': 'inline-block'}),

    html.Div([dcc.Graph(figure=pieplotfig)],
        style={'width': '99%', 'display': 'inline-block', 'border-style': 'solid', 'border-width': '0.1%', 'margin-left': '0%', 'margin-right': '0'}),
    html.Hr(),

    html.Div([
        html.H3('Versions', style={'textAlign': 'center'}),
        html.Div([dcc.Graph(id='version-graphic')],
            style={'width': '99%', 'display': 'inline-block', 'border-style': 'solid', 'border-width': '0.1%', 'margin-left': '0%', 'margin-right': '0'}),

        html.Div([dcc.Slider(1, 8, 1, value=1, id='version-slider'),],
            style={'width': '100%', 'display': 'inline-block', 'text-align':'centre'})],
        style={'width': '100%', 'display': 'inline-block'}),
    html.Hr(),

        html.Div([
        html.H3('Category Analyzer', style={'textAlign': 'center'}),
        html.Div([dcc.Dropdown(dataframe['Category'].unique(), 'ART_AND_DESIGN', id='xaxis-column'),],
            style={'width': '100%', 'display': 'inline-block', 'text-align':'centre'})],
        style={'width': '100%', 'display': 'inline-block'}),

         html.Div([dcc.Graph(id='indicator-graphic')],
        style={'width': '47%', 'display': 'inline-block', 'border-style': 'solid', 'border-width': '0.5%', 'margin-left': '0%', 'margin-right': '0'}),

        html.Div([dcc.Graph(id='installs-graphic')],
        style={'width': '47%', 'display': 'inline-block', 'border-style': 'solid', 'border-width': '0.1%', 'margin-left': '5%', 'margin-right': '0'}),
    html.Hr(),

    html.Div([
        html.H3('Correlation', style={'textAlign': 'center'}),
        html.Div([
            dcc.Dropdown(
                ['Category','Rating','Reviews','Size','Installs','Price','Content_Rating','Android_Ver'],
                'Category',
                 id='xaxis-var'),],
        style={'width': '49.5%', 'display': 'inline-block', 'align-items': 'left', 'margin-left': '0%', 'margin-right': '0'}),

    html.Div([
        dcc.Dropdown(
            ['Category','Rating','Reviews','Size','Installs','Price','Content_Rating','Android_Ver'],
            'Category',
            id='yaxis-var'),],
    style={'width': '49.5%', 'display': 'inline-block', 'margin-left': '1%', 'margin-right': '0'}),

    html.Div([dcc.Graph(id='scatterplot_variable')],
        style={'width': '99%', 'display': 'inline-block', 'border style': 'solid', 'border-width': '0.1%', 'margin-left': '0%', 'margin-right': '0'}), ], style={'width': '100%', 'display': 'inline-block'}),


#End of application's layout
])

@app.callback(
Output(component_id='version-graphic', component_property='figure'),
Input(component_id='version-slider', component_property='value')
)

def update_graph(version_number):
    y1 = dataframe.query('Android_Ver==@version_number').Category
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        y = y1,
        opacity = 0.75
    ))
    fig.update_layout(margin = {'l': 40, 'b': 40, 't': 10, 'r': 40}, bargap = 0.05, autosize = True)
    fig.update_xaxes(title = "No. of apps for android version " + str(version_number))
    fig.update_yaxes(title = "Categories")
    return fig

@app.callback(
Output(component_id='indicator-graphic',
    component_property='figure'),
Output(component_id='installs-graphic',
    component_property='figure'),
Input(component_id='xaxis-column',
    component_property='value')
)

def update_graph(xaxis_column_name):
    x1=dataframe.query('Category==@xaxis_column_name').Rating
    x2=dataframe.query('Category==@xaxis_column_name').Installs
    y2=dataframe.Installs
    fig1 = go.Figure()
    fig1.add_trace(go.Histogram(
        x=x1,
        name="Ratings",
        texttemplate="%{y}",
        textfont_size=10,
        marker_color='Purple',
        opacity=0.75
    ))
    fig1.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 40},bargap=0.05, autosize=True)
    fig1.update_xaxes(title="Rating Trends for " + str(xaxis_column_name))
    fig1.update_yaxes(title="Count of Ratings")

    fig2 = go.Figure()
    fig2.add_trace(go.Histogram(
        x=x2,
        histfunc='sum',
        name="Installs",
        marker_color='#5E42BD',
        opacity=0.75,
        hovertemplate="%{x} installations "+" for %{y} Apps"
    ))
    fig2.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 40},bargap=0.05, autosize=True)
    fig2.update_xaxes(title="Installations for " + str(xaxis_column_name))
    fig2.update_yaxes(title="Number of Apps")
    return fig1, fig2

@app.callback(
Output(component_id='scatterplot_variable',
    component_property='figure'),
Input(component_id='xaxis-var',
    component_property='value'),
Input(component_id='yaxis-var',
    component_property='value')
)
def update_graph(xaxis,yaxis):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dataframe[xaxis],
        y=dataframe[yaxis],
        mode='markers'
    ))
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 40},bargap=0.05, autosize=True)
    fig.update_xaxes(title=xaxis)
    fig.update_yaxes(title=yaxis)
    return fig

if __name__ == '__main__':
  app.run_server(debug=True, host='0.0.0.0', port=8501)

