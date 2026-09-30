import random

m, n = int(input("How many tasks are there?")), int(input("How many employees are there?"))

def generate_sample(tasks_number, employees_number):
    min_time=5
    max_time=10*60

    t=[[random.randint(min_time, max_time) for i in range(tasks_number)] for j in range(employees_number)]
    print(t)

    return t

t=generate_sample(m,n)

for i in range(n):
    for j in range(m):
        print(t[i][j], end=" ")
    print()


def encode(tasks_number, employees_number):
    p = [random.randint(0,employees_number-1) for i in range(tasks_number)]
    return p

def fitness(tasks_number, employees_number, t, population):
    
    load_on_employee = [0 for i in range(employees_number)]
    max_load=0
    for j in range(tasks_number):
        i=population[j]
        load_on_employee[i][j] += t[i][j]
        max_load=max(max_load, load_on_employee[i][j])
    
    return max_load

