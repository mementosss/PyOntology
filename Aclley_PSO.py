import numpy as np

# Функция Экли
def ackley_function(x, y):
    return (x**2 + y - 11)**2 + (x + y**2 - 7)**2

# Параметры
num_particles = 10  # Количество частиц
num_iterations = 50  # Количество итераций
w = 0.2  # Коэффициент инерции
c1 = 2.0  # Коэффициент обучения для личного лучшего
c2 = 2.0  # Коэффициент обучения для глобального лучшего
bounds = [-5, 5]  # Ограничения пространства решений

# Инициализация частиц
particles_position = np.random.uniform(bounds[0], bounds[1], (num_particles, 2))
particles_velocity = np.random.uniform(-1, 1, (num_particles, 2))
personal_best_position = np.copy(particles_position)
personal_best_value = np.array([ackley_function(x, y) for x, y in personal_best_position])
global_best_position = personal_best_position[np.argmin(personal_best_value)]
global_best_value = np.min(personal_best_value)

# Основной цикл PSO
for iteration in range(num_iterations):
    for i in range(num_particles):
        # Обновление скорости
        r1, r2 = np.random.random(), np.random.random()
        particles_velocity[i] = (
            w * particles_velocity[i]
            + c1 * r1 * (personal_best_position[i] - particles_position[i])
            + c2 * r2 * (global_best_position - particles_position[i])
        )
        # Обновление позиции
        particles_position[i] += particles_velocity[i]
        # Ограничение позиции в пределах bounds
        particles_position[i] = np.clip(particles_position[i], bounds[0], bounds[1])

        # Обновление личного лучшего
        fitness_value = ackley_function(*particles_position[i])
        if fitness_value < personal_best_value[i]:
            personal_best_value[i] = fitness_value
            personal_best_position[i] = particles_position[i]

    # Обновление глобального лучшего
    current_global_best = np.min(personal_best_value)
    if current_global_best < global_best_value:
        global_best_value = current_global_best
        global_best_position = personal_best_position[np.argmin(personal_best_value)]

    # Вывод промежуточных результатов
    if iteration < 10 or iteration % 10 == 0:
        print(
            f"Итерация {iteration + 1}: g_best = {global_best_value:.5f}, g_position = {global_best_position}"
        )

# Итоговые результаты
print("\nГлобальный минимум:")
print(f"Положение (x,y): {global_best_position}")
print(f"Значение функции f(x,y): {global_best_value:.5f}")
