import random, time, tracemalloc, matplotlib.pyplot as plt

def calculate_fitness(t, tasks_number, employees_number, ant):
    load = [0] * employees_number

    for task in range(tasks_number):
        employee = ant[task]
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


def create_ant_solution(t, tasks_number, employees_number, pheromone, alpha, beta):
   
    solution = [-1] * tasks_number

    for task_id in range(tasks_number):

        weights = []

        for emp_id in range(employees_number):

            attractiveness = 1 / t[emp_id][task_id]

            pheromone_effect = pheromone[emp_id][task_id] ** alpha
            heuristic_effect = attractiveness ** beta
            
            weights.append(pheromone_effect * heuristic_effect)

        selected_emp = choose_employee(weights)
        solution[task_id] = selected_emp

    return solution
    

def ant_colony_algorithm(t, tasks_number, employees_number, ant_count, max_iteration, alpha, beta,
                        rho, Q):
    
    pheromone_matrix = [[1.0] * tasks_number for i in range(employees_number)]

    global_best_solution = None
    global_best_score = float("inf")

    y = []
    
    for current_iteration in range(max_iteration):
        ants = []

        for i in range(ant_count):
            ant = create_ant_solution (t, tasks_number, employees_number, pheromone_matrix,
                                            alpha, beta)
            fitness = calculate_fitness(t, tasks_number, employees_number, ant)
            ants.append((fitness, ant))
            
            if fitness < global_best_score:
                global_best_score = fitness
                global_best_solution = ant.copy()

        for emp in range(employees_number):
            for task in range(tasks_number):
                pheromone_matrix[emp][task] *= rho
                
        for fitness, solution in ants:
            add = Q / fitness
            for task in range(tasks_number):
                emp = solution[task]
                pheromone_matrix[emp][task] += add
            
        y.append(global_best_score)


    for i in range(ant_count):
        ant = create_ant_solution (t, tasks_number, employees_number, pheromone_matrix,
                                   alpha, beta)
        fitness = calculate_fitness(t, tasks_number, employees_number, ant)
            
        if fitness < global_best_score:
            global_best_score = fitness
            global_best_solution = ant.copy()

    y.append(global_best_score)
    
    return (global_best_score, global_best_solution, y )



def run_aco(t, tasks_number, employees_number, runs, ants_number = 15, max_iteration = 200,
            alpha = 1.0, beta = 2.0, rho = 0.9, Q = 100.0):
    
    x_values = [i for i in range(max_iteration + 1)]
    y_values = [0 for i in range(max_iteration + 1)]
    times = []
    memories = []
    memory_times = []
    best_scores = []
    best_score = float("inf")
    best_solution = [0 for i in range(tasks_number)]
    
    for run in range(runs):
        print(f"start run {run+1} for time and best_score monitoring")
        start_time = time.perf_counter()
        score, solution, y = ant_colony_algorithm(t, tasks_number, employees_number, ants_number,
                                                  max_iteration, alpha, beta, rho, Q)                                                 
        end_time = time.perf_counter()
        times.append(end_time-start_time)
        best_scores.append(score)

        for iteration in range(len(y_values)):
            y_values[iteration] += y[iteration]
        
        if best_score > score:
            best_score = score
            best_solution = solution.copy()
    
    for iteration in range(len(y_values)):
        y_values[iteration] /= runs

    print(f"start run for memory monitoring")
    start_time = time.perf_counter()
    tracemalloc.start()
    score, solution, y = ant_colony_algorithm(t, tasks_number, employees_number, ants_number,
                                                  max_iteration, alpha, beta, rho, Q)  
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    end_time = time.perf_counter()
    memory_times.append(end_time-start_time)
    memories.append(peak/1024/1024)
    
    
    
    return dict(x_values = x_values, y_values = y_values, best_score = best_score, 
                best_solution = best_solution, times = times, memories = memories, memory_times = memory_times, best_scores = best_scores)

if __name__ == "__main__":

    def read_test(file_name):
        f = open(file_name, 'r')
        lines = f.readlines()
        f.close()
        t=[]
        employees_number, tasks_number  = lines[0].strip().split(',')
        employees_number, tasks_number = int(employees_number), int(tasks_number)
        for i in range(1,len(lines)):
            s = lines[i].strip()
            s = s[1:-1]
            t.append([int(x) for x in s.split(',')])
        return  t, tasks_number, employees_number

    file_size = input("What is the size of the file? (type s for small, m for medium, l for large): ").lower()
    while file_size not in ['s','m','l']:
        file_size = input("please type only s,m or l: ").lower()

    file_number = int(input("What is the number of the file? (type 1,2 or 3): "))
    while file_number not in [1,2,3]:
        file_number = int(input("please type only 1,2 or 3: "))

    if file_size == 's':
        file_name = f"small_test{file_number}.txt"
    elif file_size == 'm':
        file_name = f"medium_test{file_number}.txt"
    else:
        file_name = f"large_test{file_number}.txt"


    runs = int(input("How many times do you want to run the Algorithm? "
                    "(It will add another run for memory monitoring): "))

    t, m, n = read_test(file_name)
    dict_aco = run_aco(t, m, n, runs)

    f = open(f"aco_best_solution_for_{file_name}.txt", 'w')
    f.write(str(dict_aco["best_solution"]))
    f.close()

    max_time = round(max(dict_aco["times"]),4)
    min_time = round(min(dict_aco["times"]),4)
    average_time = round(sum(dict_aco["times"])/len(dict_aco["times"]),4)
    print(f"Time (seconds):  min={min_time}   max={max_time}   average={average_time}")

    max_memory = round(max(dict_aco["memories"]),4)
    min_memory = round(min(dict_aco["memories"]),4)
    average_memory = round(sum(dict_aco["memories"])/len(dict_aco["memories"]),4)
    print(f"Memory (MB):  min={min_memory}   max={max_memory}   average={average_memory}")

    max_memory_time = round(max(dict_aco["memory_times"]),4)
    min_memory_time = round(min(dict_aco["memory_times"]),4)
    average_memory_time = round(sum(dict_aco["memory_times"])/len(dict_aco["memory_times"]),4)
    print(f"Time taken with memory measuring (second):  min={min_memory_time}   max={max_memory_time}   average={average_memory_time}")
        
    max_best_score = round(max(dict_aco["best_scores"]),4)
    min_best_score = round(min(dict_aco["best_scores"]),4)
    average_best_score = round(sum(dict_aco["best_scores"])/len(dict_aco["best_scores"]),4)
    print(f"Time to Finish all tasks (minutes):  min={min_best_score}   max={max_best_score}   average={average_best_score}")

        
    plt.plot(dict_aco["x_values"], dict_aco["y_values"], linewidth = 2.0, color = 'red')
    plt.title("Ant colony Optimization's Average (best so far) fitness")
    plt.xlabel("Number of Iterations")
    plt.ylabel("Best Fitness")
    plt.show()
