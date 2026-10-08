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

def genetic_algorithm(population, fitness_function, muation_function,
                      crossover_function, mutation_probability, elite, max_iteration,
                      tasks_number, employees_number, t ):
    
    population_size = len(population)

    x = []
    y = []

    for iter in range(max_iteration):
        
        individual_scores = [(fitness_function(tasks_number, employees_number, t, ind), ind) for ind in population]
        individual_scores.sort()

        top_elite = int(elite*population_size)

        sorted_population = [ind for (fitness, ind) in individual_scores]
        population = sorted_population[:top_elite]

        x.append(iter+1)
        y.append(individual_scores[0][0])

        while (len(population)<population_size):
            prob = random.random()
            if prob < mutation_probability:

                ipos = random.randint(0, top_elite-1)

                new_individual = muation_function(employees_number, population[ipos])
                population.append(new_individual)
            
            else:
                ipos1 = random.randint(0, top_elite-1)
                ipos2 = random.randint(0, top_elite-1)

                new_individual = crossover_function(population[ipos1], population[ipos2])
                population.append(new_individual)

 
    individual_scores = [(fitness_function(tasks_number, employees_number, t, ind), ind) for ind in population]
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
    elite = 0.33
    max_iteration = 100
    population_size = 100

    file_name = 'small_test1.txt'
    m, t = read_test(file_name)
    print(t)

    times = []
    memories = []
    best_scores = []

    for run in range(runs):
        
        

        start_time = time.perf_counter()
        
        population = init_population(population_size, m, n) 
        best_score, best_solution, x, y = genetic_algorithm(population, fitness_calculation, mutation, crossover, mutation_probability, elite, max_iteration, m, n, t)

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
        best_score, best_solution, x, y = genetic_algorithm(population, fitness_calculation, mutation, crossover, mutation_probability, elite, max_iteration, m, n, t)

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        memories.append(peak/1024/1024)

    print(times)
    print(memories)
    print(best_scores)

time_and_resource_usage(7)