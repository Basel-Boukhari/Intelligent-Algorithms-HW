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