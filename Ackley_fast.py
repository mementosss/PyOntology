import numpy as np
import math
import random


# Функция Экли
def himmelblau_function(x, y):
    return (x ** 2 + y - 11) ** 2 + (x + y ** 2 - 7) ** 2


# Функция температуры (быстрое снижение)
def temperature(k, T0=100):
    return T0 / k if k > 0 else T0


# Генерация соседнего состояния с учётом границ
def neighbour(s, step_size=0.1):
    s_new = s + np.random.uniform(-step_size, step_size, size=2)
    # Ограничиваем координаты в пределах [-5, 5]
    s_new = np.clip(s_new, -5, 5)
    return s_new


# Функция вероятности перехода
def acceptance_probability(e_old, e_new, T):
    if e_new < e_old:
        return 1
    return math.exp(-(e_new - e_old) / T)


# Алгоритм имитации отжига
def simulated_annealing(func, s0, k_max=1000, T0=100, step_size=0.1):
    s = np.array(s0)
    k = 1
    last_temperature = T0  # Инициализация последней температуры

    while k <= k_max:
        T = temperature(k, T0)
        s_new = neighbour(s, step_size)
        e_old = func(*s)
        e_new = func(*s_new)

        if acceptance_probability(e_old, e_new, T) >= random.random():
            s = s_new

        # Сохраняем температуру на текущей итерации
        last_temperature = T

        # Вывод данных для первых 10 итераций
        if k <= 1000:
            print(f"Итерация {k}: x = {s[0]:.5f}, y = {s[1]:.5f}, f(x, y) = {func(*s):.5f}, T = {T:.5f}")

        k += 1

    return s, func(*s), last_temperature


# Начальные условия
s0 = [random.uniform(-5, 5), random.uniform(-5, 5)]
k_max = 10000
T0 = 100  # Начальная температура
step_size = 0.5  # Размер шага

result, value, last_temperature = simulated_annealing(himmelblau_function, s0, k_max=k_max, T0=T0, step_size=step_size)

print("\nОптимальная точка (x, y) = ", result)
print("Значение функции в оптимальной точке f(x, y) = ", value)
print("Температура на последней итерации T = ", last_temperature)
