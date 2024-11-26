import numpy as np

# Определение целевой функции (Ackley)
def ackley_function(x, y):
    return (
        -20 * np.exp(-0.2 * np.sqrt(0.5 * (x**2 + y**2)))
        - np.exp(0.5 * (np.cos(2 * np.pi * x) + np.cos(2 * np.pi * y)))
        + np.e + 20
    )

# Параметры
M = 4  # Количество частиц
L = 1000  # Количество итераций
D = 2  # Размерность задачи (2D)
T_0 = 10  # Начальная температура
search_range = [-5.0, 5.0]

# Случайная инициализация частиц
np.random.seed(42)
positions_x = np.random.uniform(search_range[0], search_range[1], M)
positions_y = np.random.uniform(search_range[0], search_range[1], M)

# Начальные значения
values = ackley_function(positions_x, positions_y)
best_value = np.min(values)
best_index = np.argmin(values)
best_position = (positions_x[best_index], positions_y[best_index])

# Итерация
for k in range(1, L + 1):
    T = T_0 / k**(1/D)  # Обновление температуры

    for i in range(M):
        # Генерация нового кандидата для каждой оси
        delta_x = np.random.standard_cauchy() * T
        delta_y = np.random.standard_cauchy() * T

        # Новые позиции
        new_position_x = positions_x[i] + delta_x
        new_position_y = positions_y[i] + delta_y

        # Убедимся, что новые позиции в пределах диапазона
        new_position_x = np.clip(new_position_x, search_range[0], search_range[1])
        new_position_y = np.clip(new_position_y, search_range[0], search_range[1])

        # Вычисление значения целевой функции
        current_value = ackley_function(new_position_x, new_position_y)

        # Принятие решения о переходе
        if current_value < best_value:
            best_value = current_value
            best_position = (new_position_x, new_position_y)

    print(f"Iteration {k}: Best Value = {best_value:.6f}, Best Position = {best_position}")

# Вывод окончательного лучшего решения
print(f"Best solution after {L} iterations: {best_position} with value {best_value:.6f}")
