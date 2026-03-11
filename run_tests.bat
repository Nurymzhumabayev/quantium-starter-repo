@echo off
setlocal enabledelayedexpansion

echo ========================================
echo    ЗАПУСК ТЕСТОВОГО НАБОРА
echo ========================================

:: 1. Активируем виртуальное окружение
echo.
echo 1. Активация виртуального окружения...

call venv\Scripts\activate.bat

if %errorlevel% neq 0 (
    echo [31m✗ Ошибка активации виртуального окружения[0m
    exit /b 1
) else (
    echo [32m✓ Виртуальное окружение активировано[0m
)

:: 2. Запускаем тесты
echo.
echo 2. Запуск тестов...

if exist "test_app.py" (
    echo Запуск pytest тестов...
    echo.
    
    pytest test_app.py -v
    
    set TEST_RESULT=%errorlevel%
) else if exist "simple_test.py" (
    echo Запуск простых тестов...
    echo.
    
    python simple_test.py
    
    set TEST_RESULT=%errorlevel%
) else (
    echo [31m✗ Не найден файл с тестами[0m
    exit /b 1
)

:: 3. Проверяем результат
echo.
echo ========================================
echo    РЕЗУЛЬТАТ
echo ========================================

if %TEST_RESULT% equ 0 (
    echo [32m✓ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО[0m
    echo [32m   Exit code: 0[0m
    exit /b 0
) else (
    echo [31m✗ ТЕСТЫ ЗАВЕРШИЛИСЬ С ОШИБКАМИ[0m
    echo [31m   Exit code: %TEST_RESULT%[0m
    exit /b 1
)