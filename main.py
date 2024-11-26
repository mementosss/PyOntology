import math
import random

# Матрица времени прохождения
time_matrix = [
    [0, 12, 18, 25, 10],
    [12, 0, 8, 14, 15],
    [18, 8, 0, 11, 17],
    [25, 14, 11, 0, 19],
    [10, 15, 17, 19, 0]
]


# Функция для вычисления длины маршрута
def calculate_route_length(route, matrix):
    length = 0
    for i in range(len(route) - 1):
        length += matrix[route[i] - 1][route[i + 1] - 1]
    return length


# Алгоритм отжига
def simulated_annealing(matrix, initial_route, initial_temp, alpha, iterations):
    current_route = initial_route
    current_temp = initial_temp
    current_length = calculate_route_length(current_route, matrix)

    print(f"Начальный маршрут: {current_route}, Длина: {current_length}, Температура: {current_temp}")

    for iteration in range(iterations):
        # Случайная перестановка
        new_route = current_route[:]
        i, j = random.sample(range(1, len(new_route) - 1), 2)
        new_route[i], new_route[j] = new_route[j], new_route[i]

        # Длина нового маршрута
        new_length = calculate_route_length(new_route, matrix)
        delta = new_length - current_length

        # Рассчитываем вероятность перехода на худшее решение
        if delta != 0:
            probability = math.exp(-delta / current_temp)
        else:
            probability = 1  # Если изменение длины 0, вероятность равна 1

        # Решение: принять или отклонить
        if delta < 0 or random.random() < probability:
            decision = "Принят"
            current_route = new_route
            current_length = new_length
        else:
            decision = "Отклонен"

        # Вывод результатов текущей итерации
        print(f"Итерация {iteration + 1}:")
        print(f"  Новый маршрут: {new_route}")
        print(f"  Длина маршрута: {new_length}")
        print(f"  Изменение длины: {delta}")
        print(f"  Вероятность принятия: {probability:.4f}")
        print(f"  Решение: {decision}")
        print(f"  Температура: {current_temp}")

        # Снижение температуры
        current_temp *= alpha

    return current_route, current_length


# Исходные данные
initial_route = [1, 3, 2, 4, 5, 1]
initial_temp = 100
alpha = 0.5
iterations = 10

# Выполнение
final_route, final_length = simulated_annealing(time_matrix, initial_route, initial_temp, alpha, iterations)
print("\nОптимальный маршрут:", final_route)
print("Длина маршрута:", final_length)
