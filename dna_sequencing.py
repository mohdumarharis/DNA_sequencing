Python 3.10.10 (v3.10.10:aad5f6a891, Feb  7 2023, 08:47:40) [Clang 13.0.0 (clang-1300.0.29.30)] on darwin
Type "help", "copyright", "credits" or "license()" for more information.

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import base64
from dash import dash_table

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Initialize the Dash app
app = dash.Dash(__name__,external_stylesheets=external_stylesheets)

# App layout
app.layout = html.Div([
    html.H1("BioClavis Assignment",        style={
            'textAlign': 'center',
            'color': '#022238'
        })
    ,html.Div(children='''
        Please Upload Your File
    '''),
    dcc.Upload(
        id='upload-data',
        children=html.Div(['Drag and Drop or ', html.A('Select File')]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False
    ),
    html.Div(id='output-data-upload'),
    html.H3("Uploaded Data Table"),
    dcc.Graph(id='sequence-graph_2'),
    html.H3("Select a Sequence"),
    dcc.Dropdown(  # Dropdown for sequence selection
        id='sequence-dropdown',
        options=[],  # This will be populated by the callback
        value=None,
        multi=False,
        placeholder="Select a Sequence"
    ),
    html.Div(id='sequence-length-display',style={'fontSize': 24}),
    html.H3("Sequence Length Plot"),
    dcc.Graph(id='sequence-graph'),
    html.H3("GC Content Analysis"),
    html.Div(id='gc-content-display',style={'fontSize': 17}) 
])


def data_to_table(d):
    split_d=[seq for seq in d.split('>') if seq]
    names = []
    sequence = []
    for n in split_d:
        lines = n.split('\n')
        names.append(lines[0])
        sequence.append(''.join(lines[1:]))
    df = pd.DataFrame({
    'Sequence_Name': names,
    'Sequence': sequence        
    })
    df['Seq_length'] = df['Sequence'].apply(len)
    return df


def atgc_df(df):
    base_columns = ["A", "T", "G", "C"]
    data = []
    for i in df["Sequence_Name"]:
        lst=[]
        n=df[df["Sequence_Name"]==i].index
        ATGC=df["Sequence"][n[0]]
        for j in base_columns:
            lst.append(ATGC.count(j))
        data.append([i] + lst)
    ATGC_df = pd.DataFrame(data, columns=["Sequence_Name"] + base_columns)
    return ATGC_df

def melted_df(df):
    return pd.melt(df, id_vars=["Sequence_Name"], var_name="Nucleotide", value_name="Count")


# function to calculate G+C content
def find_max_gc_content(seq_df, input):
    i = seq_df[seq_df["Sequence_Name"] == input].index
    ATGC = seq_df["Sequence"][i[0]]

    max_gc = 0
    max_seq_list = []
    pos_list = []

    for i in range(0, (len(ATGC) - 9)):
        seq = ATGC[i:i+10]
        gc = seq.count("G") + seq.count("C")
        if gc >= max_gc:
            max_gc = gc
            max_seq = seq
            pos = (i+1, i+11)

    for i in range(0, (len(ATGC) - 9)):
        seq = ATGC[i:i+10]
        gc = seq.count("G") + seq.count("C")
        if gc == max_gc:
            max_seq_list.append(seq)
            tup = i+1, i+11
            pos_list.append(tup)

    return {
        "Highest G+C content": max_gc,
        "Sequences with highest G+C content": max_seq_list,
        "Positions of highest G+C content": pos_list,
        "Number of Sequences with highest G+C content": len(max_seq_list)
    }


def parse_contents(contents):
    content_string = contents.split(',')[1]
    decoded = base64.b64decode(content_string).decode('utf-8')
    df=data_to_table(decoded)

    return df

# Callback to update output
# @app.callback([Output('output-data-upload', 'children'),
#                Output('sequence-graph', 'figure')],
#               [Input('upload-data', 'contents')])

@app.callback([Output('output-data-upload', 'children'),
               Output('sequence-graph_2', 'figure'),
               Output('sequence-graph', 'figure'),
               Output('sequence-dropdown', 'options'),
              Output('sequence-length-display', 'children'),
              Output('gc-content-display', 'children')],
              [Input('upload-data', 'contents'),
               Input('sequence-dropdown', 'value')])


def update_output(contents, selected_sequence):
    if contents is None:
        return [html.Div([]), {}, [],[],"",""]

    df = parse_contents(contents)
    df2=df.copy()
    
    # Create table
    table = dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{'name': i, 'id': i} for i in df.columns],page_size=2
    )

    # Create graph
    fig2 = px.bar(df, x='Sequence_Name', y='Seq_length',labels={"Sequence_Name": "Name of the Sequence",'Seq_length':"Sequence Length"}, title='Sequence Lengths')
    
    #input_setting
    dropdown_options = [{'label': seq_name, 'value': seq_name} for seq_name in df['Sequence_Name'].unique()]
...     
... 
...     # Filter data for the graph based on selected sequence
...     if selected_sequence:
...         df = df[df['Sequence_Name'] == selected_sequence]
...     
...     
...     fig = px.bar(melted_df(atgc_df(df)), x="Sequence_Name", y="Count", color="Nucleotide", 
...              title="Nucleotide Counts by Sequence", barmode="group")
...     
...     seq_length_text = ""
...     if selected_sequence:
...         selected_seq_length = df[df['Sequence_Name'] == selected_sequence]['Seq_length'].iloc[0]
...         seq_length_text = f"Length of {selected_sequence}: {selected_seq_length}"
...     
...     # Compute the GC content results for the selected sequence
...     gc_content_results = ""
...     if selected_sequence:
...         gc_content_data = find_max_gc_content(df2, selected_sequence)
...         gc_content_results = html.Div([
...             html.P(f"Highest G+C content in a Sequence of 10 : {gc_content_data['Highest G+C content']}"),
...             html.P(f"Sequences with highest G+C content : {', '.join(gc_content_data['Sequences with highest G+C content'])}"),
...             html.P(f"Positions of highest G+C content : {gc_content_data['Positions of highest G+C content']}"),
...             html.P(f"Number of Sequences of Length 10 with highest G+C content : {gc_content_data['Number of Sequences with highest G+C content']}")
...         ])
... 
... 
...     return [table, fig2, fig, dropdown_options, seq_length_text,gc_content_results]
... 
... 
... if __name__ =='__main__':
        app.run_server()
