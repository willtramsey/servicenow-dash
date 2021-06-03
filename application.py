# CONTAINER IMPORTS, NEEDED TO OPEN, UPLOAD----------------------------------------------------------------------
from azure.storage.blob import BlobServiceClient
from azure.storage.blob import ContainerClient
from azure.storage.blob import BlobClient
import pandas as pd
# CONTAINER IMPORTS, NEEDED TO OPEN, UPLOAD----------------------------------------------------------------------
# DASH IMPORTS---------------------------------------------------------------------------------------------------
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import flask_secrets
# DASH IMPORTS---------------------------------------------------------------------------------------------------

# Container Connection------------------------------------------------------------------------------------------
blob_credential = flask_secrets.blob_credential
service = BlobServiceClient(account_url="https://metrosnowblob.blob.core.windows.net/",
    credential=blob_credential)

# Container connection string
connection_string = flask_secrets.connection_string

# Container client:
container_client = ContainerClient.from_connection_string(conn_str=connection_string,
                                                          container_name="does-this-work")
# Container Connection-------------------------------------------------------------------------------------------

# support incident dataframe build ---------------------------------------------------------------------------------------------
blob = BlobClient.from_connection_string(conn_str=connection_string,
                                         container_name="does-this-work",
                                         blob_name="backlog_data_support_incidents.csv")

with open('backlog_data_support_incidents.csv', "wb") as my_blob:
    blob_data = blob.download_blob()
    blob_data.readinto(my_blob)

df = pd.read_csv('backlog_data_support_incidents.csv')

df['time'] = pd.to_datetime(df['time'])
df = df[df['time'].dt.dayofweek.isin([0,1,2,3,4])]

# support incident dataframe build ------------------------------------------------------------------------------------------

# EUC incident dataframe build ------------------------------------------------------------------------------------------------
blob = BlobClient.from_connection_string(conn_str=connection_string,
                                         container_name="does-this-work",
                                         blob_name="backlog_data_euc_incidents.csv")

with open('backlog_data_euc_incidents.csv', "wb") as my_blob:
    blob_data = blob.download_blob()
    blob_data.readinto(my_blob)

df2 = pd.read_csv('backlog_data_euc_incidents.csv')

df2['time'] = pd.to_datetime(df2['time'])
df2 = df2[df2['time'].dt.dayofweek.isin([0,1,2,3,4])]
# EUC incident dataframe build ------------------------------------------------------------------------------------------------

# EUC task dataframe build ------------------------------------------------------------------------------------------------
blob = BlobClient.from_connection_string(conn_str=connection_string,
                                         container_name="does-this-work",
                                         blob_name="backlog_data_euc_tasks.csv")

with open('backlog_data_euc_tasks.csv', "wb") as my_blob:
    blob_data = blob.download_blob()
    blob_data.readinto(my_blob)

df3 = pd.read_csv('backlog_data_euc_tasks.csv')

df3['time'] = pd.to_datetime(df3['time'])
df3 = df3[df3['time'].dt.dayofweek.isin([0,1,2,3,4])]
# EUC task dataframe build ------------------------------------------------------------------------------------------------


# Dash Build---------------------------------------------------------------------------------------------------
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
application = app.server


# fig1 ----------------------------------------------------------------------------------------------------------
fig = px.line(df, x='time', y='inc_count',
              title="Support Backlog",
              labels={
                     "inc_count": "Incident Count",
                     "time": ""
                 },)

fig.update_xaxes(
    rangebreaks=[
        dict(bounds=["sat", "mon"]), #hide weekends
    ]
)
# fig1 ----------------------------------------------------------------------------------------------------------


# fig2 ----------------------------------------------------------------------------------------------------------
fig2 = px.line(df2, x='time', y='inc_count',
              title="EUC Backlog - Incidents",
              labels={
                     "inc_count": "Incident Count",
                     "time": ""
                 },)

fig2.update_xaxes(
    rangebreaks=[
        dict(bounds=["sat", "mon"]), #hide weekends
    ]
)
# fig2 ----------------------------------------------------------------------------------------------------------


# fig3 ----------------------------------------------------------------------------------------------------------
fig3 = px.line(df3, x='time', y='inc_count',
              title="EUC Backlog - Tasks",
              labels={
                     "inc_count": "Task Count",
                     "time": ""
                 },)

fig3.update_xaxes(
    rangebreaks=[
        dict(bounds=["sat", "mon"]), #hide weekends
    ]
)
# fig3 ----------------------------------------------------------------------------------------------------------

app.layout = html.Div(children=[
    # All elements from the top of the page
    html.Div([

        html.P(['Learn about this site: ', html.A("here", href='www.google.com', target="_blank")]),
        
        html.P(['Support Center incident reporting: ', html.A("exploratory data analysis", href='https://nbviewer.jupyter.org/github/willtramsey/ServiceNow-Project-Overview/blob/main/servicenow_eda.ipynb', target="_blank"), ' and: ',
        html.A("Incident activity after 6pm", href='https://nbviewer.jupyter.org/github/willtramsey/ServiceNow-Project-Overview/blob/main/last_60_days_after_6pm.ipynb', target="_blank")]),

        html.H1(children='ServiceNow Backlog for Support and EUC'),

        html.Div(children='''
            API call ran @ 7pm nightly
        '''),

        dcc.Graph(
            id='graph1',
            figure=fig
        ),  
    ]),
    # New Div for all elements in the new 'row' of the page
    html.Div([
        html.H1(children=''),

        html.Div(children='''
            
        '''),

        dcc.Graph(
            id='graph2',
            figure=fig2
        ),  
    ]),
    html.Div([
        html.H1(children=''),

        html.Div(children='''
            
        '''),

        dcc.Graph(
            id='graph3',
            figure=fig3
        ),  
    ]),
])

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port='80')