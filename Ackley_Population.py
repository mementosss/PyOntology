import numpy as np
import random


# Целевая функция Ackley
def ackley_function(x, y):
    return (
            -20 * np.exp(-0.2 * np.sqrt(0.5 * (x ** 2 + y ** 2)))
            - np.exp(0.5 * (np.cos(2 * np.pi * x) + np.cos(2 * np.pi * y)))
            + np.e + 20
    )


# Генерация начальной популяции
def generate_population(pop_size, bounds):
    return np.random.uniform(bounds[0], bounds[1], (pop_size, 2))


# Оценка приспособленности
def fitness(population):
    return np.array([ackley_function(x, y) for x, y in population])


# Скрещивание двух родителей для создания потомка
def crossover(parent1, parent2):
    alpha = random.random()
    child = alpha * parent1 + (1 - alpha) * parent2
    return child


# Мутация потомка
def mutate(child, bounds, mutation_rate=0.1):
    if random.random() < mutation_rate:
        mutation = np.random.uniform(-1, 1, 2) * (bounds[1] - bounds[0]) * 0.1
        child += mutation
    return np.clip(child, bounds[0], bounds[1])  # Ограничение в пределах границ


# Отбор лучших особей
def selection(population, fitness_values, num_parents):
    parents_idx = np.argsort(fitness_values)[:num_parents]
    return population[parents_idx]


# Генетический алгоритм
def genetic_algorithm(pop_size, bounds, generations, num_parents):
    population = generate_population(pop_size, bounds)
    best_solution = None
    best_fitness = float('inf')

    for gen in range(generations):
        # Оценка приспособленности
        fitness_values = fitness(population)

        # Отбор родителей
        parents = selection(population, fitness_values, num_parents)

        # Новый популяции после скрещивания и мутации
        new_population = []
        while len(new_population) < pop_size:
            parent1, parent2 = random.sample(list(parents), 2)
            child = crossover(parent1, parent2)
            child = mutate(child, bounds)
            new_population.append(child)

        population = np.array(new_population)

        # Обновление лучшего решения
        min_fitness_idx = np.argmin(fitness_values)
        if fitness_values[min_fitness_idx] < best_fitness:
            best_fitness = fitness_values[min_fitness_idx]
            best_solution = population[min_fitness_idx]

        print(f"Generation {gen + 1}: Best Fitness = {best_fitness}, Best Solution = {best_solution}")

    return best_solution, best_fitness


# Параметры
pop_size = 200  # Размер популяции
bounds = (-5, 5)  # Границы для x и y
generations = 500  # Количество поколений
num_parents = 100 # Количество родителей

# Запуск генетического алгоритма
best_solution, best_fitness = genetic_algorithm(pop_size, bounds, generations, num_parents)

print(f"\nBest solution: {best_solution}")
print(f"Best fitness: {best_fitness}")
