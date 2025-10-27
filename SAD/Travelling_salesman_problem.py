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

# Функция для преобразования числового маршрута в текстовый
def route_to_text(route):
    locations = ["Пункт сбора", "Точка 1", "Точка 2", "Точка 3", "Точка 4", "Точка 5"]
    text_route = []
    for point in route:
        text_route.append(locations[point - 1])
    return " -> ".join(text_route)

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

    # Переменные для сохранения лучшего маршрута
    best_route = current_route[:]
    best_length = current_length

    print(f"Начальный маршрут: {route_to_text(initial_route)}")
    print(f"Начальная стоимость: {current_length:.2f} км")
    print("- Начало процесса отжига ---")

    for iteration in range(iterations):
        print(f"- Итерация {iteration + 1} (Температура: {current_temp:.4f}°C) ---")
        print(f"Текущий маршрут: {current_route} ({current_length:.2f} км)")

        # Случайная перестановка
        new_route = current_route[:]
        i, j = random.sample(range(1, len(new_route) - 1), 2)
        new_route[i], new_route[j] = new_route[j], new_route[i]

        # Длина нового маршрута
        new_length = calculate_route_length(new_route, matrix)
        delta = new_length - current_length

        print(f"Рабочий маршрут: {new_route} ({new_length:.2f} км)")
        print(f"Разница (ДЕ): {delta:.2f}")

        # Рассчитываем вероятность перехода на худшее решение
        if delta != 0:
            probability = math.exp(-delta / current_temp)
        else:
            probability = 1  # Если изменение длины 0, вероятность равна 1

        # Генерируем случайное число для сравнения
        r = random.random()

        # Решение: принять или отклонить
        if delta < 0:
            print("Вердикт: Решение лучше. Принимается.")
            current_route = new_route
            current_length = new_length
        else:
            print(f"Вердикт: Решение хуже. Р = {probability:.4f}, г = {r:.4f}")
            if r < probability:
                print("-> Решение принято (r < P).")
                current_route = new_route
                current_length = new_length
            else:
                print("-> Решение отклонено (r >= P).")

        # Проверяем, является ли новый маршрут лучшим
        if current_length < best_length:
            best_route = current_route[:]
            best_length = current_length
            print(f"*** Найдено новое лучшее решение! Стоимость: {best_length:.2f} ***")

        # Снижение температуры
        current_temp *= alpha
        print()

    # Возвращаем лучший маршрут и его длину
    return best_route, best_length

# Исходные данные
initial_route = [1, 3, 2, 4, 5, 1]  # Начальный маршрут (Пункт сбора -> Точка 3 -> Точка 2 -> Точка 4 -> Точка 5 -> Пункт сбора)
initial_temp = 100  # Начальная температура
alpha = 0.95  # Коэффициент уменьшения температуры
iterations = 100  # Количество итераций

# Выполнение
final_route, final_length = simulated_annealing(time_matrix, initial_route, initial_temp, alpha, iterations)

print("=== РЕЗУЛЬТАТ ===")
print(f"Самый короткий маршрут: {route_to_text(final_route)}")
print(f"Числовая последовательность: {final_route}")
print(f"Длина маршрута: {final_length:.2f} км")