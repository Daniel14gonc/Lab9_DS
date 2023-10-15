from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import calendar

df = pd.read_csv('importacion_regular.csv')
df['Fecha'] = pd.to_datetime(df['Fecha'], format='%Y-%m-%d')
pred_df = pd.read_csv('importacion_regular_test.csv')
pred_df['Fecha'] = pd.to_datetime(pred_df['Fecha'], format='%Y-%m-%d')
meses_dict = {i: calendar.month_name[i] for i in range(1, 13)}
meses_dict_sorted = {v: k for k, v in enumerate(calendar.month_name)}

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

app = Dash(__name__)

app.layout = html.Div([
    html.H1('El comportamiento de los combustibles en Guatemala a lo largo del tiempo', style={'margin-top': '30px','text-align': 'center', 'font-family': 'Helvetica'}),
    html.Div([
        html.Div([
            dcc.Graph(id='grafico-tiempo', style={'width': '50%', 'display': 'inline-block'}),
            dcc.Graph(id='grafico-barras', style={'width': '50%', 'display': 'inline-block'}),
        ]),
        html.Div([
            html.Label('Selecciona el rango de años:'),
            year_slider,
        ], style = {'font-family': 'Helvetica'}),])
], style={'background-color': '#FFF'})

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

    # figura = px.line(filtered_df, x='Fecha', y='Gasolina_regular', title='Serie de Tiempo')
    # figura.update_traces(line=dict(color='#153B50'))
    figura.update_traces(line=dict(color='#429EA6'), selector=dict(name='Gasolina_regular'))
    figura.update_traces(line=dict(color='#CC998D'), selector=dict(name='Gasolina_regular_pred'))
    
    figura.update_traces(line=dict(color='#429EA6'), selector=dict(name='Gasolina_regular'), 
                         name='Gasolina Regular')
    figura.update_traces(line=dict(color='#CC998D'), selector=dict(name='Gasolina_regular_pred'), 
                         name='Gasolina Regular Predicha')
    figura.update_yaxes(title_text='Galones importados')
    return figura

def get_monthly_data(df):
    df['Month'] = df['Fecha'].dt.month.map(meses_dict)
    df['Year'] = df['Fecha'].dt.year

    # Calcula el promedio mensual sin importar el año
    df_monthly_mean = df.groupby(['Month']).mean()

    # Opcional: Si solo deseas mantener la columna relevante (por ejemplo, 'Monto')
    df_monthly_mean = df_monthly_mean[['Gasolina_regular']]

    # Reinicia el índice para tener 'Month' como una columna en lugar de ser el índice
    df_monthly_mean.reset_index(inplace=True)
    # Ordena el DataFrame por el nombre del mes en orden alfabético
    df_monthly_mean_sorted = df_monthly_mean.sort_values(by='Month', key=lambda x: x.map(meses_dict_sorted))

    # Reinicia el índice para tener 'Month' como una columna en lugar de ser el índice
    df_monthly_mean_sorted.reset_index(drop=True, inplace=True)
    return df_monthly_mean_sorted

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
    figura.update_traces(marker_color='#153B50')
    return figura

if __name__ == '__main__':
    app.run_server(debug=True)
