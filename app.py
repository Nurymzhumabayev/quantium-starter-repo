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

# CSS стили
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                min-height: 100vh;
            }
            .main-container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }
            .header {
                background: white;
                border-radius: 15px;
                padding: 30px;
                margin-bottom: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                text-align: center;
            }
            .header h1 {
                color: #667eea;
                margin: 0;
                font-size: 2.5em;
                font-weight: 600;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
            }
            .header p {
                color: #666;
                font-size: 1.2em;
                margin: 10px 0 0 0;
            }
            .filter-container {
                background: white;
                border-radius: 15px;
                padding: 20px;
                margin-bottom: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            .filter-label {
                color: #667eea;
                font-weight: 600;
                font-size: 1.1em;
                margin-bottom: 15px;
                display: block;
            }
            .radio-group {
                display: flex;
                justify-content: space-around;
                flex-wrap: wrap;
                gap: 15px;
            }
            .radio-option {
                background: #f8f9fa;
                padding: 12px 25px;
                border-radius: 25px;
                cursor: pointer;
                transition: all 0.3s ease;
                border: 2px solid transparent;
            }
            .radio-option:hover {
                background: #e9ecef;
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
            }
            .radio-option input[type="radio"] {
                display: none;
            }
            .radio-option input[type="radio"]:checked + label {
                color: #667eea;
                font-weight: 600;
            }
            .radio-option label {
                cursor: pointer;
                color: #666;
                font-size: 1.1em;
            }
            .chart-container {
                background: white;
                border-radius: 15px;
                padding: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            .info-box {
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                border-radius: 10px;
                padding: 15px;
                margin-top: 20px;
                color: white;
                text-align: center;
                font-weight: 500;
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }
            .info-box i {
                font-style: normal;
                background: rgba(255,255,255,0.2);
                padding: 5px 10px;
                border-radius: 5px;
                margin-left: 10px;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Определяем макет приложения
app.layout = html.Div([
    html.Div([
        html.Div([
            html.H1('🍭 Pink Morsels Sales Analytics'),
            html.P('Интерактивный дашборд для анализа продаж')
        ], className='header'),
        
        html.Div([
            html.Label('Выберите регион:', className='filter-label'),
            html.Div([
                html.Div([
                    dcc.RadioItems(
                        id='region-filter',
                        options=[
                            {'label': ' Все регионы', 'value': 'all'},
                            {'label': ' Север', 'value': 'north'},
                            {'label': ' Юг', 'value': 'south'},
                            {'label': ' Запад', 'value': 'west'},
                            {'label': ' Восток', 'value': 'east'}
                        ],
                        value='all',
                        labelStyle={'display': 'inline-block', 'marginRight': '10px'},
                        style={'display': 'flex', 'justifyContent': 'space-around', 'flexWrap': 'wrap'}
                    )
                ], className='radio-group')
            ])
        ], className='filter-container'),
        
        html.Div([
            dcc.Graph(id='sales-chart')
        ], className='chart-container'),
        
        html.Div([
            html.Span('📊 Вертикальная линия показывает 15 января 2021 - дату повышения цены')
        ], className='info-box')
        
    ], className='main-container')
])

# Callback для обновления графика
@app.callback(
    Output('sales-chart', 'figure'),
    Input('region-filter', 'value')
)
def update_chart(selected_region):
    # Фильтруем данные по региону
    if selected_region == 'all':
        filtered_df = df
        title = 'Продажи Pink Morsels по всем регионам'
    else:
        filtered_df = df[df['region'] == selected_region]
        title = f'Продажи Pink Morsels в регионе: {selected_region}'
    
    # Создаем график
    fig = px.line(filtered_df, x='date', y='sales',
                  title=title,
                  labels={'date': 'Дата', 'sales': 'Продажи ($)'},
                  color='region' if selected_region == 'all' else None)
    
    # Добавляем вертикальную линию для даты изменения цены
    fig.add_vline(x='2021-01-15', line_width=2, line_dash="dash",
                  line_color="red", opacity=0.7)
    
    # Добавляем аннотацию
    fig.add_annotation(x='2021-01-15', y=filtered_df['sales'].max() * 0.9,
                       text="Повышение цены<br>15 января 2021",
                       showarrow=True,
                       arrowhead=1,
                       ax=-50,
                       ay=-30,
                       font=dict(color="red", size=12))
    
    # Настраиваем внешний вид
    fig.update_layout(
        xaxis_title='Дата',
        yaxis_title='Продажи (доллары)',
        font=dict(family='Segoe UI', size=12),
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
        title=dict(font=dict(size=20, color='#667eea')),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

# Запускаем приложение
if __name__ == '__main__':
    app.run(debug=True)