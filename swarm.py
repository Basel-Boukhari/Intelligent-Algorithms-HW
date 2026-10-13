import random, matplotlib.pyplot as plt


def Calculate_cost (t, bird, tasks_number, employees_number):
    cost = 0
    load = [0 for i in range(employees_number)]
    for j in range(tasks_number):
        i = bird[j]
        load[i] += t[i][j]     
        cost = max(cost, load[i])
    return cost


def PSO(t, birds_number, tasks_number, employees_number, iterations_number,w, c1, c2):

    x = []
    y = []

    birds = [[random.randint(0, employees_number - 1) for i in range(tasks_number)] for i in range(birds_number)]
    gbest = float("inf")
    solution_gbest = [0 for i in range(tasks_number)]
    pbests = [Calculate_cost(t, birds[i], tasks_number, employees_number) for i in range(birds_number)]
    solutions_pbests = [list(bird) for bird in birds]
    velocity = [[random.uniform(-1, 1) for i in range(tasks_number)] for _ in range(birds_number)]

    for i in range(birds_number):
        if (gbest > pbests[i]):
            gbest = pbests[i]
            solution_gbest = list(birds[i])

    x.append(0)
    y.append(gbest)

    for iteration in range(iterations_number):
        for i in range(birds_number):
            for j in range(tasks_number):
                rand1 = random.random()
                rand2 = random.random()
                velocity[i][j] = (velocity[i][j] + c1 * rand1 * (solutions_pbests[i][j] - birds[i][j]) +
                                c2 * rand2 * (solution_gbest[j] - birds[i][j]))
                velocity[i][j] = max(-birds[i][j], velocity[i][j])
                velocity[i][j] = min(velocity[i][j], employees_number -1 - birds[i][j])
                birds[i][j] = birds[i][j] + velocity[i][j]
                birds[i][j] = round(birds[i][j])
                if birds[i][j] < 0:
                    birds[i][j] = 0
                if birds[i][j] > employees_number - 1:
                    birds[i][j] = employees_number - 1
        for i in range(birds_number):
            current_bird_fitness = Calculate_cost(t, birds[i], tasks_number, employees_number)
            if current_bird_fitness < pbests[i]:
                pbests[i] = current_bird_fitness
                solutions_pbests[i] = list(birds[i])
            if current_bird_fitness < gbest:
                gbest = current_bird_fitness
                solution_gbest = list(birds[i])
                
        x.append(iteration+1)
        y.append(gbest)
        
    return gbest, solution_gbest, x, y



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

file_name = "large_test8.txt"
tasks_number, t = read_test(file_name)
employees_number = 4
birds_number = 30
iterations_number = 50
w = 0.7
c1 = 5.0
c2 = 5.0
gbest, solution_gbest, x, y = PSO(t, birds_number, tasks_number, employees_number,iterations_number,w, c1, c2)

print(f"(gbest): {gbest}")
# print(f"(best solution is): {solution_gbest}")

plt.plot(x, y)
plt.show()

