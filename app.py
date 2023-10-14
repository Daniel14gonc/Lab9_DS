from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go

# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')
# print(df.head())
df = pd.read_csv('importacion_regular.csv')

app = Dash(__name__)

app.layout = html.Div([
    html.H1('Gráfico de Serie de Tiempo'),
    dcc.Graph(id='grafico-tiempo'),
])

# Callback para actualizar el gráfico en función de los filtros
@app.callback(
    Output('grafico-tiempo', 'figure'),
    [Input('grafico-tiempo', 'relayoutData')]
)
def update_graph(relayoutData):
    figura = px.line(df, x='Fecha', y='Gasolina_regular', title='Serie de Tiempo')
    return figura

if __name__ == '__main__':
    app.run(debug=True)
