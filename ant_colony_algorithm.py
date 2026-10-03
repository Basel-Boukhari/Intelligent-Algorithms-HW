import random
import matplotlib.pyplot as plt


def generate_sample(tasks_number, employees_number):
    min_time = 5
    max_time = 10 * 60

    t = [
        [random.randint(min_time, max_time) for _ in range(tasks_number)]
        for _ in range(employees_number)
    ]

    return t


def fitness_calculation(tasks_number, employees_number, t, individual):
    load = [0 for _ in range(employees_number)]
    fitness = 0

    for j in range(tasks_number):
        i = individual[j]
        load[i] += t[i][j]
        fitness = max(fitness, load[i])

    return fitness


def choose_employee(probabilities):
    total = sum(probabilities)
    value = random.random() * total
    current = 0

    for employee in range(len(probabilities)):
        current += probabilities[employee]
        if value <= current:
            return employee

    return len(probabilities) - 1


def create_ant_solution(
    tasks_number,
    employees_number,
    t,
    pheromone,
    alpha,
    beta
):
    individual = [-1 for _ in range(tasks_number)]
    load = [0 for _ in range(employees_number)]

    tasks_order = list(range(tasks_number))
    random.shuffle(tasks_order)

    for task in tasks_order:
        probabilities = []

        for employee in range(employees_number):
            new_makespan = max(
                max(load),
                load[employee] + t[employee][task]
            )

            heuristic = 1 / max(new_makespan, 1)
            probability = (
                pheromone[employee][task] ** alpha
                * heuristic ** beta
            )
            probabilities.append(probability)

        employee = choose_employee(probabilities)
        individual[task] = employee
        load[employee] += t[employee][task]

    return individual


def ant_colony_algorithm(
    tasks_number,
    employees_number,
    t,
    ant_count,
    max_iteration,
    alpha,
    beta,
    evaporation_rate,
    Q
):
    pheromone = [
        [1.0 for _ in range(tasks_number)]
        for _ in range(employees_number)
    ]

    best_solution = None
    best_score = float("inf")

    x = []
    y = []

    for iteration in range(max_iteration):
        ant_solutions = []

        for ant in range(ant_count):
            individual = create_ant_solution(
                tasks_number,
                employees_number,
                t,
                pheromone,
                alpha,
                beta
            )

            score = fitness_calculation(
                tasks_number,
                employees_number,
                t,
                individual
            )

            ant_solutions.append((score, individual))

        iteration_best_score, iteration_best_solution = min(
            ant_solutions,
            key=lambda item: item[0]
        )

        if iteration_best_score < best_score:
            best_score = iteration_best_score
            best_solution = iteration_best_solution.copy()

        for employee in range(employees_number):
            for task in range(tasks_number):
                pheromone[employee][task] *= (1 - evaporation_rate)

        deposit = Q / max(iteration_best_score, 1)

        for task in range(tasks_number):
            employee = iteration_best_solution[task]
            pheromone[employee][task] += deposit

        x.append(best_score)
        y.append(iteration)

    return best_score, best_solution, x, y

m = int(input("How many tasks are there? "))
n = int(input("How many employees are there? "))

ant_count = 50
max_iteration = 30
alpha = 1.0
beta = 2.0
evaporation_rate = 0.1
Q = 100.0

t = generate_sample(m, n)

best_score, best_solution, x, y = ant_colony_algorithm(
    m,
    n,
    t,
    ant_count,
    max_iteration,
    alpha,
    beta,
    evaporation_rate,
    Q
)

print(best_solution, best_score, sep="    ")

plt.plot(y, x, marker="o")
plt.xlabel("Iteration")
plt.ylabel("Best Fitness")
plt.title("Ant Colony Optimization")
plt.show()
