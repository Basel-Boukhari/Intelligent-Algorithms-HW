import random,time, tracemalloc, matplotlib.pyplot as plt

def create_individual(tasks_number, employees_number):
    p = [random.randint(0,employees_number-1) for i in range(tasks_number)]
    return p

def fitness_calculation(tasks_number, employees_number, t, individual):
    
    load = [0 for i in range(employees_number)]
    fitness=0
    for j in range(tasks_number):
        i=individual[j]
        load[i] += t[i][j]
        fitness=max(fitness, load[i])
    
    return fitness

def mutation(employees_number, individual):
    ipos = random.randint(0,len(individual)-1)

    new_employee=[random.randint(0,employees_number-1)]

    individual = individual[:ipos] + new_employee + individual[ipos+1:]

    return individual

def crossover(individual_1, individual_2):
    ipos=random.randint(1,len(individual_1)-2)

    new_individual = individual_1[:ipos] + individual_2[ipos:]

    return new_individual

def init_population(population_size, tasks_number, employees_number):
    population = []
    for i in range(population_size):
        individual = create_individual(tasks_number, employees_number)
        population.append(individual)
    return population

def genetic_algorithm(population, population_size, parents_size, fitness_function, mutation_function,
                      mutation_probability, crossover_function, crossover_probability, 
                      elite, max_iteration, tasks_number, employees_number, t ):
    
    x = []
    y = []

    for iter in range(max_iteration):
        
        
        individual_scores = [(fitness_function(tasks_number, employees_number, t, ind), ind)
                             for ind in population]
        individual_scores.sort()

        x.append(iter+1)
        y.append(individual_scores[0][0])

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

            crossover_prob = random.random()
            if crossover_prob < crossover_probability:
                ipos1 = random.randint(0, parents_size-1)
                ipos2 = random.randint(0, parents_size-1)
                new_individual = crossover_function(parents[ipos1], parents[ipos2])
            
            else:
                ipos = random.randint(0, parents_size-1)
                new_individual = parents[ipos].copy()
            
            mutation_prob = random.random()
            if mutation_prob < mutation_probability:
                new_individual = mutation_function(employees_number, new_individual)
            
            new_population.append(new_individual)                


        population = new_population

    individual_scores = [(fitness_function(tasks_number, employees_number, t, ind), ind)
                         for ind in population]
    individual_scores.sort()


    return (individual_scores[0][0], individual_scores[0][1], x, y)

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

def time_and_resource_usage(runs):

    n = 4
    mutation_probability = 0.3
    crossover_probability = 0.6
    elite = 0.33
    max_iteration = 100
    population_size = 100
    parents_size = 5

    file_name = 'large_test8.txt'
    m, t = read_test(file_name)
    #print(t)

    times = []
    memories = []
    best_scores = []

    for run in range(runs):
        
        

        start_time = time.perf_counter()
        
        population = init_population(population_size, m, n) 
        best_score, best_solution, x, y = genetic_algorithm(population, population_size, parents_size,
                                                            fitness_calculation, mutation, mutation_probability,
                                                            crossover, crossover_probability, elite,
                                                            max_iteration, m, n, t)                              
        end_time = time.perf_counter()
        times.append(end_time-start_time)
        best_scores.append(best_score)

        plt.plot(x, y, linewidth = 1.5)
        plt.title("Genetic Algorithm's best solution for every iteration")
        plt.xlabel("Number of Iterations")
        plt.ylabel("Best Solution")
        plt.show()
    
    for run in range(runs):

        tracemalloc.start()

        population = init_population(population_size, m, n)
        best_score, best_solution, x, y = genetic_algorithm(population, population_size, parents_size,
                                                            fitness_calculation, mutation, mutation_probability,
                                                            crossover, crossover_probability, elite,
                                                            max_iteration, m, n, t)

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        memories.append(peak/1024/1024)

        print(f"finished run {run+1} for memory tracing")

    print(times)
    print(memories)
    print(best_scores)

time_and_resource_usage(7)