from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import calendar

# Cargar los datos modelo 1
df = pd.read_csv('importacion_regular.csv')
df['Fecha'] = pd.to_datetime(df['Fecha'], format='%Y-%m-%d')
pred_df = pd.read_csv('importacion_regular_test.csv')
pred_df['Fecha'] = pd.to_datetime(pred_df['Fecha'], format='%Y-%m-%d')


# Cargar los datos modelo 2
df1 = pd.read_csv('diesel.csv')
df1['Fecha'] = pd.to_datetime(df1['Fecha'], format='%Y-%m-%d')
pred_df1 = pd.read_csv('diesel_test.csv')
pred_df1['Fecha'] = pd.to_datetime(pred_df1['Fecha'], format='%Y-%m-%d')

# Cargar los datos modelo 3
df2 = pd.read_csv('super.csv')
df2['Fecha'] = pd.to_datetime(df2['Fecha'], format='%Y-%m-%d')
pred_df2 = pd.read_csv('super_test.csv')
pred_df2['Fecha'] = pd.to_datetime(pred_df2['Fecha'], format='%Y-%m-%d')


meses_dict = {i: calendar.month_name[i] for i in range(1, 13)}
meses_dict_sorted = {v: k for k, v in enumerate(calendar.month_name)}
names = ['Predicción de importación de gasolina regular', 'Predicción de consumo de diesel', 'Predicción de precio de gasolina súper']

id_graph = 'grafico-tiempo'

# Crear un control deslizante para seleccionar años
available_years = df['Fecha'].dt.year.unique()
year_slider = dcc.RangeSlider(
    id='year-slider',
    min=min(available_years),
    max=max(available_years),
    step=1,
    marks={str(year): str(year) for year in available_years},
    value=[min(available_years), max(available_years)]
)

# Crear un control deslizante para seleccionar años
available_years1 = df1['Fecha'].dt.year.unique()
year_slider1 = dcc.RangeSlider(
    id='year-slider',
    min=min(available_years1),
    max=max(available_years1),
    step=1,
    marks={str(year): str(year) for year in available_years1},
    value=[min(available_years1), max(available_years1)]
)

# Crear un control deslizante para seleccionar años
available_years2 = df2['Fecha'].dt.year.unique()
year_slider2 = dcc.RangeSlider(
    id='year-slider',
    min=min(available_years2),
    max=max(available_years2),
    step=1,
    marks={str(year): str(year) for year in available_years2},
    value=[min(available_years2), max(available_years2)]
)

app = Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    html.H1('El comportamiento de los combustibles en Guatemala a lo largo del tiempo', style={'margin-top': '30px','text-align': 'center', 'font-family': 'Helvetica'}),
    dcc.Dropdown(names, names[0], id='dropdown-action', style = {'font-family': 'Helvetica', 'width': '70%', 'margin': 'auto', 'margin-top': '30px', 'margin-bottom': '30px'}),
    html.Div(id='output-div'),
], style={'background-color': '#ECEBE4'})

@app.callback(
    Output('output-div', 'children'),
    [Input('dropdown-action', 'value')]
)
def execute_action(selected_action):
    global id_graph
    if selected_action == names[0]:
        return  html.Div([
                    html.Div([
                        dcc.Graph(id='grafico-tiempo', style={'width': '50%', 'display': 'inline-block'}),
                        dcc.Graph(id='grafico-barras', style={'width': '50%', 'display': 'inline-block'}),
                    ]),
                    html.Div([
                        html.Label('Selecciona el rango de años:'),
                        year_slider,
                    ], style = {'font-family': 'Helvetica'}),
                ])
    elif selected_action == names[1]:
        return  html.Div([
                    html.Div([
                        dcc.Graph(id='grafico-tiempo1', style={'width': '50%', 'display': 'inline-block'}),
                        dcc.Graph(id='grafico-barras1', style={'width': '50%', 'display': 'inline-block'}),
                    ]),
                    html.Div([
                        html.Label('Selecciona el rango de años:'),
                        year_slider1,
                    ], style = {'font-family': 'Helvetica'}),
                ])
    else:
        return  html.Div([
                    html.Div([
                        dcc.Graph(id='grafico-tiempo2', style={'width': '50%', 'display': 'inline-block'}),
                        dcc.Graph(id='grafico-barras2', style={'width': '50%', 'display': 'inline-block'}),
                    ]),
                    html.Div([
                        html.Label('Selecciona el rango de años:'),
                        year_slider2,
                    ], style = {'font-family': 'Helvetica'}),
                ])

# Callback para actualizar el gráfico de serie de tiempo en función de los filtros
@app.callback(
    Output('grafico-tiempo2', 'figure'),
    [Input('grafico-tiempo2', 'relayoutData'),
     Input('year-slider', 'value')]
)
def update_time_series_graph(relayoutData, selected_years):
    filtered_df = df2[(df2['Fecha'].dt.year >= selected_years[0]) & (df2['Fecha'].dt.year <= selected_years[1])]

    merged_df = pd.merge(filtered_df, pred_df2, on='Fecha', how='left')
    # merged_df['Superior_pred'] = merged_df['Gasolina regular']
    # merged_df.drop(columns=['Gasolina regular'], inplace=True)
    figura = px.line(merged_df, x='Fecha', y=['Superior', 'Superior_pred'], 
                     title='Costo de gasolina súper en Quetzales', labels={'Superior': 'Gasolina Superior', 'Superior_pred': 'Gasolina superior predicha'},)
    figura.update_layout(paper_bgcolor='#ECEBE4')
    # figura = px.line(filtered_df, x='Fecha', y='Gasolina_regular', title='Serie de Tiempo')
    # figura.update_traces(line=dict(color='#153B50'))
    figura.update_traces(line=dict(color='#153B50'), selector=dict(name='Superior'))
    figura.update_traces(line=dict(color='#CC998D'), selector=dict(name='Superior_pred'))
    
    figura.update_traces(line=dict(color='#153B50'), selector=dict(name='Superior'), 
                         name='Gasolina Superior Real')
    figura.update_traces(line=dict(color='#CC998D'), selector=dict(name='Superior_pred'), 
                         name='Gasolina Superior Predicha')
    figura.update_yaxes(title_text='Quetzalez')
    return figura

# Callback para actualizar el gráfico de serie de tiempo en función de los filtros
@app.callback(
    Output('grafico-tiempo1', 'figure'),
    [Input('grafico-tiempo1', 'relayoutData'),
     Input('year-slider', 'value')]
)
def update_time_series_graph(relayoutData, selected_years):
    filtered_df = df1[(df1['Fecha'].dt.year >= selected_years[0]) & (df1['Fecha'].dt.year <= selected_years[1])]

    merged_df = pd.merge(filtered_df, pred_df1, on='Fecha', how='left')
    merged_df['Diesel_conjunto_pred'] = merged_df['Diesel conjunto']
    merged_df.drop(columns=['Diesel conjunto'], inplace=True)

    figura = px.line(merged_df, x='Fecha', y=['Diesel_conjunto', 'Diesel_conjunto_pred'], 
                     title='Diesel conjunto importada en galones', labels={'Diesel_conjunto': 'Diesel', 'Gasolina_regular_pred': 'Diesel predicho'})
    figura.update_layout(paper_bgcolor='#ECEBE4')
    # figura = px.line(filtered_df, x='Fecha', y='Gasolina_regular', title='Serie de Tiempo')
    # figura.update_traces(line=dict(color='#153B50'))
    figura.update_traces(line=dict(color='#153B50'), selector=dict(name='Diesel_conjunto'))
    figura.update_traces(line=dict(color='#CC998D'), selector=dict(name='Diesel_conjunto_pred'))
    
    figura.update_traces(line=dict(color='#153B50'), selector=dict(name='Diesel_conjunto'), 
                         name='Diesel consumido real')
    figura.update_traces(line=dict(color='#CC998D'), selector=dict(name='Diesel_conjunto_pred'), 
                         name='Diesel Conjunto Predicho')
    figura.update_yaxes(title_text='Diesel consumido predicho')
    return figura

# Callback para actualizar el gráfico de serie de tiempo en función de los filtros
@app.callback(
    Output('grafico-tiempo', 'figure'),
    [Input('grafico-tiempo', 'relayoutData'),
     Input('year-slider', 'value')]
)
def update_time_series_graph(relayoutData, selected_years):
    filtered_df = df[(df['Fecha'].dt.year >= selected_years[0]) & (df['Fecha'].dt.year <= selected_years[1])]

    merged_df = pd.merge(filtered_df, pred_df, on='Fecha', how='left')
    merged_df['Gasolina_regular_pred'] = merged_df['Gasolina regular']
    merged_df.drop(columns=['Gasolina regular'], inplace=True)

    figura = px.line(merged_df, x='Fecha', y=['Gasolina_regular', 'Gasolina_regular_pred'], 
                     title='Gasolina regular importada en galones', labels={'Gasolina_regular': 'Gasolina Completa', 'Gasolina_regular_pred': 'Gasolina regular predicha'})
    figura.update_layout(paper_bgcolor='#ECEBE4')
    # figura = px.line(filtered_df, x='Fecha', y='Gasolina_regular', title='Serie de Tiempo')
    # figura.update_traces(line=dict(color='#153B50'))
    figura.update_traces(line=dict(color='#153B50'), selector=dict(name='Gasolina_regular'))
    figura.update_traces(line=dict(color='#CC998D'), selector=dict(name='Gasolina_regular_pred'))
    
    figura.update_traces(line=dict(color='#153B50'), selector=dict(name='Gasolina_regular'), 
                         name='Gasolina Regular')
    figura.update_traces(line=dict(color='#CC998D'), selector=dict(name='Gasolina_regular_pred'), 
                         name='Gasolina Regular Predicha')
    figura.update_yaxes(title_text='Galones importados')
    return figura

def get_monthly_data(df, column='Gasolina_regular'):
    df['Month'] = df['Fecha'].dt.month.map(meses_dict)
    df['Year'] = df['Fecha'].dt.year

    # Calcula el promedio mensual sin importar el año
    df_monthly_mean = df.groupby(['Month']).mean()

    # Opcional: Si solo deseas mantener la columna relevante (por ejemplo, 'Monto')
    df_monthly_mean = df_monthly_mean[[column]]

    # Reinicia el índice para tener 'Month' como una columna en lugar de ser el índice
    df_monthly_mean.reset_index(inplace=True)
    # Ordena el DataFrame por el nombre del mes en orden alfabético
    df_monthly_mean_sorted = df_monthly_mean.sort_values(by='Month', key=lambda x: x.map(meses_dict_sorted))

    # Reinicia el índice para tener 'Month' como una columna en lugar de ser el índice
    df_monthly_mean_sorted.reset_index(drop=True, inplace=True)
    return df_monthly_mean_sorted

# Callback para actualizar el gráfico de barras en función de los filtros
@app.callback(
    Output('grafico-barras2', 'figure'),
    [Input('grafico-tiempo2', 'relayoutData'),
     Input('year-slider', 'value')]
)
def update_bar_chart(relayoutData, selected_years):
    filtered_df = df2[(df2['Fecha'].dt.year >= selected_years[0]) & (df2['Fecha'].dt.year <= selected_years[1])]
    df_monthly = get_monthly_data(filtered_df, 'Superior')
    figura = px.bar(df_monthly, x=df_monthly['Month'], y='Superior', title='Gráfico de Barras (Promedio Mensual)')
    figura.update_yaxes(title_text='Quetzales')
    figura.update_layout(paper_bgcolor='#ECEBE4')
    figura.update_traces(marker_color='#429EA6')
    return figura

# Callback para actualizar el gráfico de barras en función de los filtros
@app.callback(
    Output('grafico-barras1', 'figure'),
    [Input('grafico-tiempo1', 'relayoutData'),
     Input('year-slider', 'value')]
)
def update_bar_chart(relayoutData, selected_years):
    filtered_df = df1[(df1['Fecha'].dt.year >= selected_years[0]) & (df1['Fecha'].dt.year <= selected_years[1])]
    df_monthly = get_monthly_data(filtered_df, 'Diesel_conjunto')
    figura = px.bar(df_monthly, x=df_monthly['Month'], y='Diesel_conjunto', title='Gráfico de Barras (Promedio Mensual)')
    figura.update_yaxes(title_text='Galones importados')
    figura.update_layout(paper_bgcolor='#ECEBE4')
    figura.update_traces(marker_color='#429EA6')
    return figura

# Callback para actualizar el gráfico de barras en función de los filtros
@app.callback(
    Output('grafico-barras', 'figure'),
    [Input('grafico-tiempo', 'relayoutData'),
     Input('year-slider', 'value')]
)
def update_bar_chart(relayoutData, selected_years):
    filtered_df = df[(df['Fecha'].dt.year >= selected_years[0]) & (df['Fecha'].dt.year <= selected_years[1])]
    df_monthly = get_monthly_data(filtered_df)
    figura = px.bar(df_monthly, x=df_monthly['Month'], y='Gasolina_regular', title='Gráfico de Barras (Promedio Mensual)')
    figura.update_yaxes(title_text='Galones importados')
    figura.update_layout(paper_bgcolor='#ECEBE4')
    figura.update_traces(marker_color='#429EA6')
    return figura

if __name__ == '__main__':
    app.run_server(debug=True)
