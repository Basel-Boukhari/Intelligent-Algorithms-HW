import random



def generate_sample(tasks_number, employees_number):
    min_time=5
    max_time=10*60

    t=[[random.randint(min_time, max_time) for i in range(tasks_number)] for j in range(employees_number)]
    print(t)

    return t


""" for i in range(n):
    for j in range(m):
        print(t[i][j], end=" ")
    print() """


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
    ipos = random.randint(0,len(individual))

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

    for _ in range(max_iteration):
        
############        print(population)
        individual_scores = [(fitness_function(tasks_number, employees_number, t, ind), ind) for ind in population]
        individual_scores.sort()

        top_elite = int(elite*population_size)

        sorted_population = [ind for (fitness, ind) in individual_scores]
        population = sorted_population[:top_elite]

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

###########        print("iteration %d is finished" %(_))
 
    individual_scores = [(fitness_function(tasks_number, employees_number, t, ind), ind) for ind in population]
    individual_scores.sort()
    print(individual_scores[0][0], individual_scores[0][1], sep = "    ")
    return (individual_scores[0][0], individual_scores[0][1])

m, n = int(input("How many tasks are there?")), int(input("How many employees are there?"))
mutation_probability = 0.1
elite = 0.1
max_iteration = 30
population_size = 50

t = generate_sample(m,n)

population = init_population(population_size, m, n)

# print (population)

genetic_algorithm(population, fitness_calculation, mutation, crossover, mutation_probability, elite, max_iteration, m, n, t)
