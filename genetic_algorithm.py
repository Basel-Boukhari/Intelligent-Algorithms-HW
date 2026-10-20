import random, time, tracemalloc, matplotlib.pyplot as plt

def create_individual(tasks_number, employees_number):
    individual = [random.randint(0,employees_number-1) for i in range(tasks_number)]
    return individual

def calculate_fitness(t, tasks_number, employees_number, individual):
    load = [0 for i in range(employees_number)]
    fitness=0
    for j in range(tasks_number):
        i=individual[j]
        load[i] += t[i][j]
        fitness=max(fitness, load[i])
    return fitness

def mutation(tasks_number, employees_number, individual, mutation_probability):
    new_individual = individual.copy()
    for j in range(tasks_number):
        if random.random() < mutation_probability:
            new_individual[j] = random.randint(0, employees_number-1)
    return new_individual

def crossover(tasks_number, individual_1, individual_2):
    ipos=random.randint(1,tasks_number - 2)
    new_individual = individual_1[:ipos] + individual_2[ipos:]
    return new_individual

def init_population(tasks_number, employees_number, population_size):
    population = []
    for i in range(population_size):
        individual = create_individual(tasks_number, employees_number)
        population.append(individual)
    return population

def genetic_algorithm(t, tasks_number, employees_number, population_size, parents_size, max_iteration,
                      fitness_function, mutation_function, mutation_probability, crossover_function,
                      crossover_probability, elite):
                      
    best_fitness = float("inf")
    y = []

    population = init_population(tasks_number, employees_number, population_size)

    for iteration in range(max_iteration):

        individual_scores = [(fitness_function(t, tasks_number, employees_number, ind), ind) 
                             for ind in population]
        individual_scores.sort()

        best_fitness = min(best_fitness, individual_scores[0][0])
        y.append(best_fitness)

        weights = [1.0/fitness for fitness, ind in individual_scores]
        total_weight = sum(weights)

        parents = []
        for i in range(parents_size):
            val = random.random() * total_weight
            for j in range(population_size):
                val -= weights[j]
                if val <= 0:
                    parents.append(individual_scores[j][1])
                    break
        
        sorted_population = [ind for (fitness, ind) in individual_scores]
        top_elite = int(elite*population_size)
        new_population = sorted_population[:top_elite]

        while (len(new_population)<population_size):

            if random.random() < crossover_probability:
                ipos1 = random.randint(0, parents_size-1)
                ipos2 = random.randint(0, parents_size-1)
                new_individual = crossover_function(tasks_number, parents[ipos1], parents[ipos2])
            
            else:
                ipos = random.randint(0, parents_size-1)
                new_individual = parents[ipos].copy()
            

            new_individual = mutation_function(tasks_number, employees_number,
                                               new_individual, mutation_probability)
            
            new_population.append(new_individual)

        population = new_population.copy()


    individual_scores = [(fitness_function(t, tasks_number, employees_number, ind), ind) 
                             for ind in population]
    individual_scores.sort()

    best_fitness = min(best_fitness, individual_scores[0][0])
    y.append(best_fitness)
    best_solution = individual_scores[0][1]
    
    return (best_fitness, best_solution, y)


def run_ga(t, tasks_number, employees_number, runs, population_size = 100, parents_size = 20,
                              max_iteration = 200, fitness_function = calculate_fitness,
                              mutation_function = mutation, mutation_probability = 0.005,
                              crossover_function = crossover, crossover_probability = 0.7, elite = 0.1 ):

    x_values = [i for i in range(max_iteration + 1)]
    y_values = [0 for i in range(max_iteration + 1)]
    times = []
    memories = []
    best_scores = []
    best_score = float("inf")
    best_solution = [0 for i in range(tasks_number)]
    
    for run in range(runs):
        print(f"start run {run+1} for time and best_score monitoring")
        start_time = time.perf_counter()
        score, solution, y = genetic_algorithm(t, tasks_number, employees_number, population_size, parents_size, max_iteration,
                                fitness_function, mutation_function, mutation_probability, crossover_function,
                                crossover_probability, elite)                                                   
        end_time = time.perf_counter()
        times.append(end_time-start_time)
        best_scores.append(score)

        for iteration in range(len(y_values)):
            y_values[iteration] += y[iteration]
        
        if best_score > score:
            best_score = score
            best_solution = solution.copy()
    
    for run in range(runs):
        print(f"start run {run+1} for memory monitoring")
        tracemalloc.start()
        score, solution, y = genetic_algorithm(t, tasks_number, employees_number, population_size, parents_size, max_iteration,
                                fitness_function, mutation_function, mutation_probability, crossover_function,
                                crossover_probability, elite)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        memories.append(peak/1024/1024)
    
    for iteration in range(len(y_values)):
            y_values[iteration] /= runs
    
    return dict(x_values = x_values, y_values = y_values, best_score = best_score, 
                best_solution = best_solution, times = times, memories = memories, best_scores = best_scores)


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
                    "(It will run double the times you typed, one for time monitoring and one for memory monitoring): "))

    t, m, n = read_test(file_name)
    dict_ga = run_ga(t, m, n, runs)

    f = open(f"ga_best_solution_for_{file_name}.txt", 'w')
    f.write(str(dict_ga["best_solution"]))
    f.close()

    max_time = round(max(dict_ga["times"]),4)
    min_time = round(min(dict_ga["times"]),4)
    average_time = round(sum(dict_ga["times"])/len(dict_ga["times"]),4)
    print(f"Time (seconds):  min={min_time}   max={max_time}   average={average_time}")

    max_memory = round(max(dict_ga["memories"]),4)
    min_memory = round(min(dict_ga["memories"]),4)
    average_memory = round(sum(dict_ga["memories"])/len(dict_ga["memories"]),4)
    print(f"Memory (MB):  min={min_memory}   max={max_memory}   average={average_memory}")
        
    max_best_score = round(max(dict_ga["best_scores"]),4)
    min_best_score = round(min(dict_ga["best_scores"]),4)
    average_best_score = round(sum(dict_ga["best_scores"])/len(dict_ga["best_scores"]),4)
    print(f"Time to Finish all tasks (minutes):  min={min_best_score}   max={max_best_score}   average={average_best_score}")


    plt.plot(dict_ga["x_values"], dict_ga["y_values"], linewidth = 2.0, color = 'blue')
    plt.title("Genetic Algorithm's Average (best so far) Fitness")
    plt.xlabel("Number of Iterations")
    plt.ylabel("Best Fitness")
    plt.show()