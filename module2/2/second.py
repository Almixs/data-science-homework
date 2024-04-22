import pandas as pd

def fill_avg_salary(dataframe, position_col='Посада', salary_col='salary'):
    """
    Функція для агрегації даних за посадою та обчислення мінімальної, максимальної та середньої зарплати для кожної посади.

    Параметри:
    dataframe (DataFrame): DataFrame, що містить дані про зарплати та посади спеціалістів.
    position_col (str): Назва стовпця, що містить посади.
    salary_col (str): Назва стовпця, що містить зарплату.

    Повертає:
    DataFrame: DataFrame з результатами агрегації за посадою та мінімальною, максимальною та середньою зарплатою.
    """
    aggregated_data = dataframe.groupby(position_col)[salary_col].agg(['min', 'max', 'mean']).reset_index()
    return aggregated_data

# Зчитуємо дані з CSV-файлу
df = pd.read_csv("2017_jun_final - 2017_jun_final.csv")

# Виводимо початкові рядки, розмір та типи даних
print(df.head())
print(df.shape)
print(df.dtypes)

# Обчислюємо частку пропусків у кожній колонці
missing_values = df.isnull().sum()
total_rows = len(df)
missing_ratio = (missing_values / total_rows) * 100
print("Частка пропусків в кожній колонці:")
print(missing_ratio)

# Видаляємо рядки з пропусками у всіх стовпцях, крім "Мова програмування"
df_cleaned = df.dropna(subset=df.columns.difference(['Мова програмування']))

# Обчислюємо частку пропусків у кожній колонці після видалення пропусків
missing_values_cleaned = df_cleaned.isnull().sum()
total_rows_cleaned = len(df_cleaned)
missing_ratio_cleaned = (missing_values_cleaned / total_rows_cleaned) * 100

print("Частка пропусків в кожній колонці після видалення пропусків, крім 'Мова програмування':")
print(missing_ratio_cleaned)

# Групуємо дані за "Мова програмування" == "Python"
python_data = df.loc[df['Мова програмування'] == 'Python']

# Викликаємо функцію fill_avg_salary для обчислення агрегованих даних про зарплати
aggregated_data = fill_avg_salary(python_data, position_col='Посада', salary_col='salary')

# Створюємо новий DataFrame з результатами агрегації
new_df = pd.DataFrame({
    'Посада': aggregated_data['Посада'],
    'Мін. зп': aggregated_data['min'],
    'Макс. зп': aggregated_data['max'],
    'avg': aggregated_data['mean']
})

# Описова статистика для стовпчика "avg"
describe_stats = new_df['avg'].describe()

# Додавання описової статистики до нового DataFrame
new_df.loc['LOL don`t understand last task'] = describe_stats

# Виводимо новий DataFrame з описовою статистикою
print(new_df)

new_df.to_csv('aggregated_salary_stats.csv', index=False)