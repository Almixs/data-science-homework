import pandas as pd
import matplotlib.pyplot as plt

match = 'Коефіцієнт народжуваності в регіонах України'
info = pd.read_html('https://uk.wikipedia.org/wiki/%D0%9D%D0%B0%D1%81%D0%B5%D0%BB%D0%B5%D0%BD%D0%BD%D1%8F_%D0%A3%D0%BA%D1%80%D0%B0%D1%97%D0%BD%D0%B8',
                    thousands="",
                    decimal=",",
                    match=match)

# Заміна значень "—" на NaN у всіх таблицях DataFrame
cleaned_dfs = [df.replace("—", pd.NA) for df in info]

# Об'єднання всіх таблиць у один DataFrame
combined_df = pd.concat(cleaned_dfs)

# Заміна типів нечислових колонок на числові
for col in combined_df.columns:
    if pd.api.types.is_object_dtype(combined_df[col]):
        try:
            combined_df[col] = pd.to_numeric(combined_df[col])
        except ValueError:
            pass

# Видалення останнього рядка
combined_df.drop(combined_df.index[-1], inplace=True)

print(combined_df.head())
print(combined_df.shape)
print(combined_df.dtypes)

# Визначення частки пропусків у кожній колонці
missing_values = combined_df.isnull().sum()
total_values = len(combined_df)
missing_ratio = missing_values / total_values
print("Частка пропусків у колонцях:")
print(missing_ratio)

# Заміна відсутніх даних середніми значеннями по стовпцях, крім першого
filled_df = combined_df.copy()
filled_df.iloc[:, 1:] = filled_df.iloc[:, 1:].fillna(filled_df.iloc[:, 1:].mean())
print(filled_df)

# Обчислення середніх значень для кожного стовпця (крім першого з назвами областей)
avg_values = filled_df.iloc[:, 1:].mean()

# Отримання значення середньої народжуваності в 2019 році по Україні
avg_birth_rate_2019 = avg_values["2019"]

# Отримання списку регіонів з вищим за середній рівнем народжуваності у 2019 році
regions_above_avg = filled_df[filled_df["2019"] > avg_birth_rate_2019]["Регіон"].tolist()

print(regions_above_avg)

# Знаходження регіону з найвищим рівнем народжуваності у 2014 році
highest_birth_rate_2014_region = filled_df["2014"].idxmax()
region_name = filled_df.loc[highest_birth_rate_2014_region, 'Регіон']
print("Регіон з найвищим рівнем народжуваності у 2014 році:", region_name)

regions = filled_df['Регіон']
birth_rate_2019 = filled_df['2019']

# Побудова стовпчикової діаграми
plt.barh(regions, birth_rate_2019, color='skyblue')
plt.xlabel('Коефіцієнт народжуваності')
plt.title('Народжуваність по регіонах у 2019 році')
plt.gca().invert_yaxis()  # Реверсія осі Y, щоб регіони були в порядку зростання від верху до низу

plt.savefig("birth_rate_2019_plot.png")
