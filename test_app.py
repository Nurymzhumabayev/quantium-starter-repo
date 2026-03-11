import pytest
from dash import Dash
import dash.testing as dt
from app import app  # импортируем само приложение

def test_header_present(dash_duo):
    """Тест проверяет, что заголовок присутствует"""
    dash_duo.start_server(app)
    
    # Ждем загрузки страницы
    dash_duo.wait_for_element(".header h1", timeout=10)
    
    # Проверяем заголовок
    header = dash_duo.find_element(".header h1")
    assert header is not None
    assert "Pink Morsels" in header.text
    
    print("✓ Заголовок найден")

def test_visualization_present(dash_duo):
    """Тест проверяет, что график присутствует"""
    dash_duo.start_server(app)
    
    # Ждем загрузки графика
    dash_duo.wait_for_element("#sales-chart", timeout=10)
    
    # Проверяем график
    chart = dash_duo.find_element("#sales-chart")
    assert chart is not None
    
    print("✓ График найден")

def test_region_picker_present(dash_duo):
    """Тест проверяет, что выбор региона присутствует"""
    dash_duo.start_server(app)
    
    # Ждем загрузки радио-кнопок
    dash_duo.wait_for_element("#region-filter", timeout=10)
    
    # Проверяем радио-кнопки
    radio = dash_duo.find_element("#region-filter")
    assert radio is not None
    
    # Проверяем наличие опций
    options = dash_duo.find_elements("input[type='radio']")
    assert len(options) >= 5
    
    print("✓ Выбор региона найден")