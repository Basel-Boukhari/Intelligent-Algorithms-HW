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


def encode(tasks_number, employees_number):
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

    new_employee=random.randint(0,employees_number-1)

    individual = individual[:ipos] + new_employee + individual[ipos+1:]

    return individual

def crossover(individual_1, individual_2):
    ipos=random.randint(1,len(individual_1)-2)

    new_individual = individual_1[:ipos] + individual_2[ipos+1:]

    return new_individual

def init_population():
    return

def genetic_algorithm(population, fitness_function, muation_function,
                      crossover_function, mutation_probability, elite, max_iteration):
    
    return

m, n = int(input("How many tasks are there?")), int(input("How many employees are there?"))
mutation_probability = 0.1
elite = 2
max_iteration = 30

t=generate_sample(m,n)

population = init_population()

genetic_algorithm(population, fitness_calculation, mutation, crossover, mutation_probability, elite, max_iteration)
