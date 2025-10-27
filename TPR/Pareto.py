import numpy as np
import pandas as pd

df = pd.DataFrame({
    'Цена услуги (руб.)': [261000, 190000, 130000, 150000, 125000, 210000, 200000, 115000, 180000, 160000],
    'Время выполнения услуги (час.)': [30, 24, 32, 30, 48, 28, 36, 48, 24, 30],
    'Отзывы (от 1 до 5)': [4.5, 4.9, 4.9, 4.7, 4.8, 4.7, 4.7, 4.4, 4.6, 5.0],
    'Стаж работы автомаляра (год)': [15, 12, 4, 8, 9, 17, 10, 9, 13, 12]})

df.index = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10']
print("Исходные данные:")
print(df)

# Сохраняем копию с исходными значениями для вывода
df_original = df.copy()

# Преобразуем для сравнения (критерии минимизации -> максимизации)
df_for_comparison = df.copy()
df_for_comparison['Цена услуги (руб.)'] = 1 / df_for_comparison['Цена услуги (руб.)']
df_for_comparison['Время выполнения услуги (час.)'] = 1 / df_for_comparison['Время выполнения услуги (час.)']

# Создаем массив для хранения результатов попарного сравнения
arr1 = np.zeros((10, 10))
arr1 = arr1.astype("object")

# Попарное сравнение альтернатив (используем преобразованные данные)
for i in range(10):
    for j in range(i + 1, 10):
        arr = df_for_comparison.iloc[i].values >= df_for_comparison.iloc[j].values
        check = all(x == True for x in arr)
        arr2 = df_for_comparison.iloc[i].values <= df_for_comparison.iloc[j].values
        check2 = all(x == True for x in arr2)

        if check == True:
            arr1[j, i] = 'A' + str(i + 1)
        elif check2 == True:
            arr1[j, i] = 'A' + str(j + 1)
        else:
            arr1[j, i] = 'н'

# Создаем новый DataFrame для результатов попарного сравнения
df_ = pd.DataFrame(arr1, columns=['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10'])
df_.index = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10']

print("\nТаблица: Попарное сравнение альтернатив:")
print(df_)

# ВЫВОДИМ ПАРЕТО-ОПТИМАЛЬНЫЕ АЛЬТЕРНАТИВЫ С ИСХОДНЫМИ ЗНАЧЕНИЯМИ
print("\nВывод парето-оптимальных альтернатив (исходные значения):")
print(df_original.iloc[[1, 5, 9]])

# Дальнейший код остается без изменений...
print(
    "\nРезультат указания верхней/нижней границы: ('Цена услуги (руб.)' >= 200000 , 'Время выполнения услуги (час.)' < 28)")

print(
    "\nРезультат отбора вариантов, удовлетворяющих заданным критериям: главный критерий: Цена услуги (руб.), Отзывы (от 1 до 5) >= 4.6, Время выполнения услуги (час.) < 32")
print(df_original[(df_original['Отзывы (от 1 до 5)'] > 4.6) & (df_original['Время выполнения услуги (час.)'] < 32)])


def lex_optimization(df):
    max_crit = df['Стаж работы автомаляра (год)'].max()
    optimal_df = df[df['Стаж работы автомаляра (год)'] == max_crit]

    if len(optimal_df) == 1:
        return optimal_df

    next_crit = df.loc[optimal_df.index]['Время выполнения услуги (час.)'].max()
    optimal_df = optimal_df[optimal_df['Время выполнения услуги (час.)'] == next_crit]

    return optimal_df


result = lex_optimization(df_original)
print("\nРезультат лексикографической оптимизации: (Самая важная: Стаж работы автомаляра (год))")
print(result)