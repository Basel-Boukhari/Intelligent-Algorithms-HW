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
    load = [0] * employees_number

    for task in range(tasks_number):
        employee = individual[task]
        load[employee] += t[employee][task]

    return max(load)

def choose_employee(weights):

    total = sum(weights)
    value = random.random() * total
    current = 0

    for employee in range(len(weights)):
        current += weights[employee]
        if value <= current:
            return employee

    return len(weights) - 1


def create_ant_solution(
    tasks_number,
    employees_number,
    t,
    pheromone,
    alpha,
    beta
):
    
    solution = [-1] * tasks_number
    load = [0] * employees_number

    task_indices = [i for i in range(tasks_number)]
    random.shuffle(task_indices)

    for task_id in task_indices:

        weights = []
        
        for emp_id in range(employees_number):

            predicted_load = load[emp_id] + t[emp_id][task_id]
            #attractiveness = 1 / max(predicted_load, 1)
            #attractiveness = 1/ (t[emp_id][task_id] * max(predicted_load,1))
            attractiveness = 1 / t[emp_id][task_id]

            pheromone_effect = pheromone[emp_id][task_id] ** alpha
            heuristic_effect = attractiveness ** beta
            
            weights.append(pheromone_effect * heuristic_effect)

        selected_emp = choose_employee(weights)
        solution[task_id] = selected_emp
        load[selected_emp] += t[selected_emp][task_id]

    return solution
    

def ant_colony_algorithm(
    tasks_number,
    employees_number,
    t,
    ant_count,
    max_iteration,
    alpha,
    beta,
    rho,
    Q
):
    pheromone_matrix = [
        [1.0] * tasks_number
        for _ in range(employees_number)
    ]

    global_best_solution = None
    global_best_score = float("inf")

    best_scores = []
    iterations = []
    for current_iteration in range(max_iteration):
        solutions = []

        for _ in range(ant_count):
            solution = create_ant_solution(
                tasks_number,
                employees_number,
                t,
                pheromone_matrix,
                alpha,
                beta
            )

            fitness = fitness_calculation(
                tasks_number,
                employees_number,
                t,
                solution
            )

            solutions.append((fitness, solution))
            
            if fitness < global_best_score:
                global_best_score = fitness
                global_best_solution = solution.copy()

        for emp in range(employees_number):
            for task in range(tasks_number):
                pheromone_matrix[emp][task] *= (1 - rho)
                
        for fitness, solution in solutions:
            add = Q / max(fitness,1)
            for task in range(tasks_number):
                emp = solution[task]
                pheromone_matrix[emp][task] += add
            
        best_scores.append(global_best_score)
        iterations.append(current_iteration)

    return (
        global_best_score,
        global_best_solution,
        best_scores,
        iterations
    )


def read_test(file_name):
    f = open(file_name, 'r')
    lines = f.readlines()
    f.close()
    t=[]
    tasks_number = int(lines[0].strip())
    for i in range(1,len(lines)):
        s = lines[i].strip()
        s = s[1:-1]
        t.append([int(x) for x in s.split(',')])
    return tasks_number, t



ant_count = 15
max_iteration = 100
alpha = 1.0
beta = 10.0
rho = 0.5
Q = 100.0

file_name = 'large_test8.txt'
n = 4
m , t = read_test(file_name)

best_score, best_solution, best_scores, iterations = ant_colony_algorithm(
    m,
    n,
    t,
    ant_count,
    max_iteration,
    alpha,
    beta,
    rho,
    Q
)

print("Best assignment:", best_solution)
print("Best load:", best_score, "minutes")

plt.plot(iterations, best_scores, marker="o")
plt.xlabel("Iteration")
plt.ylabel("max load (minutes)")
plt.title("Ant Colony Optimization")
plt.show()
