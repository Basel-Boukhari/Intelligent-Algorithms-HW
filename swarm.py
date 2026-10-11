import random

tasks_min = [[10,20,30,50,70,80],[20,23,33,56,60,30],[30,10,33,55,89,58]]

num_birds = 30

num_loops = 50

birds = [[random.randint(0, len(tasks_min) - 1) for i in range(len(tasks_min[0]))] for i in range(num_birds)]

loads = [[0 for i in range(len(tasks_min))]for i in range(num_birds)]

gbest_calc = 0

gbest = [0 for i in range(len(tasks_min[0]))]

pbests_calc = [0 for i in range(num_birds)]

pbest = [list(bird) for bird in birds]

velocity = [[random.uniform(-1, 1) for i in range(len(tasks_min[0]))] for _ in range(num_birds)]

c1 = 2.0
c2 = 2.0


def Calculate_Load (tasks_min, bird, load):
    for i in range(len(tasks_min)):
        for j in range(len(tasks_min[0])):
            if (bird[j] == tasks_min.index(tasks_min[i])):
                load[i] += tasks_min[i][j]
    return load


for i in range(num_birds):
    loads[i] = Calculate_Load(tasks_min, birds[i], loads[i])

def Calculate_Pbest (pbest, load):
    for i in range(len(tasks_min)):
        if (load[i] > pbest):
            pbest = load[i]
    return pbest

for i in range(num_birds):
    pbests_calc[i] = Calculate_Pbest(pbests_calc[i], loads[i])
gbest_calc = pbests_calc[0]
gbest = list(birds[0])
for i in range(num_birds):
    if (gbest_calc > pbests_calc[i]):
        gbest_calc = pbests_calc[i]
        gbest = list(birds[i])
    



for iteration in range(num_loops):
    for i in range(num_birds):
        for j in range(len(tasks_min[0])):
            rand1 = random.random()
            rand2 = random.random()
            velocity[i][j] = (velocity[i][j] + c1 * rand1 * (pbest[i][j] - birds[i][j]) + c2 * rand2 * (gbest[j] - birds[i][j]))
            birds[i][j] = birds[i][j] + velocity[i][j]
            birds[i][j] = round(birds[i][j])
            if birds[i][j] < 0:
                birds[i][j] = 0
            if birds[i][j] > len(tasks_min) - 1:
                birds[i][j] = len(tasks_min) - 1
    loads = [[0 for i in range(len(tasks_min))] for i in range(num_birds)]
    for i in range(num_birds):
        loads[i] = Calculate_Load(tasks_min, birds[i], loads[i])
        current_bird_fitness = Calculate_Pbest(0, loads[i])
        if current_bird_fitness < pbests_calc[i]:
            pbests_calc[i] = current_bird_fitness
            pbest[i] = list(birds[i])
        if current_bird_fitness < gbest_calc:
            gbest_calc = current_bird_fitness
            gbest = list(birds[i])
            
print(f"(gbest): {gbest}")
print(f"(Makespan): {gbest_calc}")