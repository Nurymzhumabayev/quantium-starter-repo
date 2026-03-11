import pandas as pd
import glob
 
# Находим все CSV файлы в папке data
csv_files = glob.glob('data/daily_sales_data_*.csv')

# Создаем пустой список для хранения данных
all_data = []

# Обрабатываем каждый файл
for file in csv_files:
    # Читаем CSV
    df = pd.read_csv(file)
    
    # Оставляем только Pink Morsels
    df = df[df['product'] == 'pink morsel']
    
    # Создаем колонку sales (цена * количество)
    # Убираем $ из цены и превращаем в число
    df['price'] = df['price'].replace('[\$,]', '', regex=True).astype(float)
    df['sales'] = df['quantity'] * df['price']
    
    # Оставляем только нужные колонки
    df = df[['sales', 'date', 'region']]
    
    # Добавляем в общий список
    all_data.append(df)

# Объединяем все данные
final_df = pd.concat(all_data, ignore_index=True)

# Сортируем по дате (опционально)
final_df = final_df.sort_values('date')

# Сохраняем в новый CSV
final_df.to_csv('formatted_sales.csv', index=False)

print("Готово! Файл сохранен как formatted_sales.csv")
print(f"Всего записей: {len(final_df)}")