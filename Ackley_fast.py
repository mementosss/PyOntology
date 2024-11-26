import numpy as np


# Определение целевой функции Экли
def ackley_function(x, y):
    return (
            -20 * np.exp(-0.2 * np.sqrt(0.5 * (x ** 2 + y ** 2)))
            - np.exp(0.5 * (np.cos(2 * np.pi * x) + np.cos(2 * np.pi * y)))
            + np.e + 20
    )


# Инициализация параметров
M = 4 # Количество частиц
L = 10  # Количество итераций
alpha = 0.95
beta = 0.2
gamma = 0.6
search_range = [-5, 5]  # Интервал поиска решений для x и y

# Случайная инициализация частиц
np.random.seed(42)  # Для воспроизводимости
positions_x = np.random.uniform(search_range[0], search_range[1], M)
positions_y = np.random.uniform(search_range[0], search_range[1], M)
velocities_x = np.zeros(M)
velocities_y = np.zeros(M)

# Вычисление начальных значений функции
values = ackley_function(positions_x, positions_y)
best_value = np.min(values)
best_index = np.argmin(values)
best_position = (positions_x[best_index], positions_y[best_index])

# Вывод начальных условий
print("На примере четырех частиц покажем работу алгоритма в течение одной итерации. Начальные условия:")
print(f"1. Количество частиц: M = {M};")
print(f"2. Количество итераций: L = {L};")
print(f"3. Параметры в изменении скорости: α = {alpha}, β ={beta}, γ = {gamma}.")
print(
    f"Интервал поиска решений: x ∈ [{search_range[0]}; {search_range[1]}], y ∈ [{search_range[0]}; {search_range[1]}].")
print("Случайным образом проинициализируем стартовые положения частиц так, чтобы они принадлежали данному диапазону:")

for i in range(M):
    print(f"x{i + 1}(0) = ({positions_x[i]:.4f}), y{i + 1}(0) = ({positions_y[i]:.4f}).")
    print(f"f(x{i + 1}(0), y{i + 1}(0)) = {values[i]:.4f}, ")

print(f"Лучшее значение целевой функции f(x{best_index + 1}(0), y{best_index + 1}(0)) = {best_value:.6f}")

# Итерация
for iteration in range(L):
    print(f"\n--- Итерация {iteration + 1} ---")  # Вывод номера текущей итерации
    for i in range(M):
        # Обновляем скорость
        velocities_x[i] = beta * velocities_x[i] + gamma * np.random.uniform(-1, 1)
        velocities_y[i] = beta * velocities_y[i] + gamma * np.random.uniform(-1, 1)

        # Обновляем положение
        new_position_x = positions_x[i] + velocities_x[i]
        new_position_y = positions_y[i] + velocities_y[i]

        # Убеждаемся, что частицы остаются в диапазоне
        new_position_x = np.clip(new_position_x, search_range[0], search_range[1])
        new_position_y = np.clip(new_position_y, search_range[0], search_range[1])

        # Вычисляем значение функции
        current_value = ackley_function(new_position_x, new_position_y)

        # Обновляем лучшее значение
        if current_value < best_value:
            best_value = current_value
            best_position = (new_position_x, new_position_y)

        # Вывод для текущей частицы
        print(f"{i + 1}) Обновим скорость {i + 1}-й частицы по x: v_x({iteration + 1}) = {velocities_x[i]:.4f};")
        print(f"Обновим скорость {i + 1}-й частицы по y: v_y({iteration + 1}) = {velocities_y[i]:.4f};")
        print(
            f"Обновим позицию {i + 1}-й частицы по x: x{i + 1}({iteration + 1}) = x{i + 1}(0) + v_x({iteration + 1}) = {new_position_x:.4f}.")
        print(
            f"Обновим позицию {i + 1}-й частицы по y: y{i + 1}({iteration + 1}) = y{i + 1}(0) + v_y({iteration + 1}) = {new_position_y:.4f}.")
        print(f"После работы с {i + 1}-й частицей лучшее значение целевой функции f̂ = {best_value:.4f}.\n")

        # Обновляем текущую позицию
        positions_x[i] = new_position_x
        positions_y[i] = new_position_y
