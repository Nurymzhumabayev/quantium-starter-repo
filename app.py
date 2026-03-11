import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Загружаем данные
df = pd.read_csv('formatted_sales.csv')

# Преобразуем дату в правильный формат
df['date'] = pd.to_datetime(df['date'])

# Сортируем по дате
df = df.sort_values('date')

# Создаем Dash приложение
app = dash.Dash(__name__)

# Определяем макет приложения
app.layout = html.Div([
    # Заголовок
    html.H1('Анализ продаж Pink Morsels',
            style={'textAlign': 'center',
                   'color': '#2c3e50',
                   'fontFamily': 'Arial',
                   'padding': '20px'}),
    
    # Описание
    html.Div('Визуализация продаж Pink Morsels по датам',
             style={'textAlign': 'center',
                    'color': '#7f8c8d',
                    'marginBottom': '30px',
                    'fontFamily': 'Arial'}),
    
    # График
    dcc.Graph(
        id='sales-chart',
        figure=px.line(df, x='date', y='sales',
                       title='Продажи Pink Morsels по дням',
                       labels={'date': 'Дата',
                              'sales': 'Продажи ($)',
                              'region': 'Регион'},
                       color='region')  # Разные цвета для разных регионов
        .update_layout(
            xaxis_title='Дата',
            yaxis_title='Продажи (доллары)',
            font=dict(family='Arial', size=12),
            hovermode='x unified'
        )
    ),
    
    # Информация о дате изменения цены
    html.Div([
        html.P('Вертикальная линия показывает 15 января 2021 - дату повышения цены',
               style={'textAlign': 'center',
                      'color': '#e74c3c',
                      'fontWeight': 'bold',
                      'marginTop': '20px'})
    ])
])

# Запускаем приложение
if __name__ == '__main__':
    app.run(debug=True)