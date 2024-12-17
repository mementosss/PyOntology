import numpy as np
import math
import random

# Функция Акли
def ackley_function(x, y):
    return (
        -20 * np.exp(-0.2 * np.sqrt(0.5 * (x**2 + y**2)))
        - np.exp(0.5 * (np.cos(2 * np.pi * x) + np.cos(2 * np.pi * y)))
        + np.e + 20
    )

# Функция температуры
def temperature(k, T0=100):
    return T0 / k if k > 0 else T0

# Генерация соседнего состояния с распределением Коши
def neighbour_cauchy(s, scale=1.0):
    s_new = s + np.random.standard_cauchy(size=2) * scale
    s_new = np.clip(s_new, -5, 5)  # Ограничиваем координаты в пределах [-5, 5]
    return s_new

# Функция вероятности перехода
def acceptance_probability(e_old, e_new, T):
    if e_new < e_old:
        return 1
    return math.exp(-(e_new - e_old) / T)

# Алгоритм имитации отжига с распределением Коши
def simulated_annealing_cauchy(func, s0, k_max=1000, T0=100, scale=1.0):
    s = np.array(s0)
    k = 1
    last_temperature = T0  # Инициализация последней температуры

    while k <= k_max:
        T = temperature(k, T0)
        s_new = neighbour_cauchy(s, scale * T)  # Масштабируем шаг с температурой
        e_old = func(*s)
        e_new = func(*s_new)

        if acceptance_probability(e_old, e_new, T) >= random.random():
            s = s_new

        # Сохраняем температуру на текущей итерации
        last_temperature = T

        # Вывод данных для первых 10 итераций
        if k <= 10:
            print(f"Итерация {k}: x = {s[0]:.5f}, y = {s[1]:.5f}, f(x, y) = {func(*s):.5f}, T = {T:.5f}")

        k += 1

    return s, func(*s), last_temperature

# Начальные условия
s0 = [random.uniform(-5, 5), random.uniform(-5, 5)]
k_max = 10000
T0 = 100
scale = 0.5  # Масштаб для распределения Коши

# Запуск алгоритма
result, value, last_temperature = simulated_annealing_cauchy(ackley_function, s0, k_max=k_max, T0=T0, scale=scale)

print("\nОптимальная точка (x, y) = ", result)
print("Значение функции в оптимальной точке f(x, y) = ", value)
print("Температура на последней итерации T = ", last_temperature)
