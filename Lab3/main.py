import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html

# Завантаження даних
data = pd.read_csv('bitcoin_price.csv')

# Створення Dash-додатку
app = dash.Dash(__name__)

# Макет додатку
app.layout = html.Div([
    html.H1("Залежність ціни акцій від часу"),
    dcc.Dropdown(
        id='stock-dropdown',
        options=[
            {'label': 'Bitcoin', 'value': 'Bitcoin'},
            {'label': 'Apple', 'value': 'Apple'},
            {'label': 'Tesla', 'value': 'Tesla'}
        ],
        value='Bitcoin'
    ),
    dcc.Graph(id='stock-graph')
])

# Оновлення графіку на основі вибраної акції
@app.callback(
    dash.dependencies.Output('stock-graph', 'figure'),
    [dash.dependencies.Input('stock-dropdown', 'value')]
)
def update_graph(stock):
    filtered_data = data[data['Stock'] == stock]
    fig = px.line(filtered_data, x='Date', y='Price', title=f'Ціна акцій {stock}')
    return fig

# Запуск додатку
if __name__ == '__main__':
    app.run_server(debug=True)