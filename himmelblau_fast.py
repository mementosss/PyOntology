import random
import math


def himmelblau_function(x, y):
    return (x**2 + y - 11)**2 + (x + y**2 - 7)**2

def simulated_annealing(initial_temp, final_temp, alpha):
    curr_temp = initial_temp
    curr_solution = (3, 3)
    curr_energy = himmelblau_function(curr_solution[0], curr_solution[1])
    while curr_temp > final_temp:
        new_solution = (round(random.uniform(-5, 5), 6), round(random.uniform(-5, 5), 6))
        new_energy = himmelblau_function(new_solution[0], new_solution[1])
        heat = new_energy - curr_energy
        if heat > 0:
            probability = initial_temp * math.pow(math.e, -(heat/curr_temp))
            random_probability = random.random() * 100
            if random_probability <= probability:
                curr_solution, curr_energy = new_solution, new_energy
        else:
            curr_solution, curr_energy = new_solution, new_energy
        curr_temp *= alpha
    return curr_solution, curr_energy
