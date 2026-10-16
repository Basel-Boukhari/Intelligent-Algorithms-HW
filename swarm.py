import random, time, tracemalloc, matplotlib.pyplot as plt


def calculate_fitness (t, bird, tasks_number, employees_number):
    cost = 0
    load = [0 for i in range(employees_number)]
    for j in range(tasks_number):
        i = bird[j]
        load[i] += t[i][j]     
        cost = max(cost, load[i])
    return cost


def PSO(t, tasks_number, employees_number, birds_number, iterations_number, c1, c2):

    y = []

    birds = [[random.randint(0, employees_number - 1) for i in range(tasks_number)] for i in range(birds_number)]
    gbest = float("inf")
    solution_gbest = [0 for i in range(tasks_number)]
    pbests = [calculate_fitness(t, birds[i], tasks_number, employees_number) for i in range(birds_number)]
    solutions_pbests = [list(bird) for bird in birds]
    velocity = [[random.uniform(-1, 1) for i in range(tasks_number)] for _ in range(birds_number)]

    for i in range(birds_number):
        if (gbest > pbests[i]):
            gbest = pbests[i]
            solution_gbest = list(birds[i])


    for iteration in range(iterations_number):
        for i in range(birds_number):
            for j in range(tasks_number):
                rand1 = random.random()
                rand2 = random.random()
                velocity[i][j] = (velocity[i][j] + c1 * rand1 * (solutions_pbests[i][j] - birds[i][j]) +
                                c2 * rand2 * (solution_gbest[j] - birds[i][j]))
                velocity[i][j] = min(velocity[i][j], 2)
                velocity[i][j] = max(velocity[i][j], -2)
                birds[i][j] = birds[i][j] + velocity[i][j]
                birds[i][j] = round(birds[i][j])
                if birds[i][j] < 0:
                    birds[i][j] = 0
                if birds[i][j] > employees_number - 1:
                    birds[i][j] = employees_number - 1
        for i in range(birds_number):
            current_bird_fitness = calculate_fitness(t, birds[i], tasks_number, employees_number)
            if current_bird_fitness < pbests[i]:
                pbests[i] = current_bird_fitness
                solutions_pbests[i] = list(birds[i])
            if current_bird_fitness < gbest:
                gbest = current_bird_fitness
                solution_gbest = list(birds[i])
                
        y.append(gbest)
        
    return gbest, solution_gbest, y

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


def run_pso(t, tasks_number, employees_number, runs):

    birds_number = 30
    max_iteration = 200
    c1 = 2.0
    c2 = 2.0
    
    x_values = [i for i in range(1,max_iteration + 1)]
    y_values = [0 for i in range(max_iteration)]
    times = []
    memories = []
    best_scores = []
    best_score = float("inf")
    best_solution = [0 for i in range(tasks_number)]
    
    for run in range(runs):
        print(f"start run {run+1} for time and best_score monitoring")
        start_time = time.perf_counter()
        score, solution, y = PSO(t, tasks_number, employees_number, birds_number, max_iteration, c1, c2)                                                      
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
        score, solution, y = PSO(t, tasks_number, employees_number, birds_number, max_iteration, c1, c2)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        memories.append(peak/1024/1024)
    
    
    return dict(x_values = x_values, y_values = y_values, best_score = best_score, 
                best_solution = best_solution, times = times, memories = memories, best_scores = best_scores)


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
dict_pso = run_pso(t, m, n, runs)

f = open("pso_best_solution.txt", 'w')
f.write(str(dict_pso["best_solution"]))
f.close()

max_time = round(max(dict_pso["times"]),4)
min_time = round(min(dict_pso["times"]),4)
average_time = round(sum(dict_pso["times"])/len(dict_pso["times"]),4)
print(f"Time (seconds):  min={min_time}   max={max_time}   average={average_time}")

max_memory = round(max(dict_pso["memories"]),4)
min_memory = round(min(dict_pso["memories"]),4)
average_memory = round(sum(dict_pso["memories"])/len(dict_pso["memories"]),4)
print(f"Memory (MB):  min={min_memory}   max={max_memory}   average={average_memory}")
    
max_best_score = round(max(dict_pso["best_scores"]),4)
min_best_score = round(min(dict_pso["best_scores"]),4)
average_best_score = round(sum(dict_pso["best_scores"])/len(dict_pso["best_scores"]),4)
print(f"Time to Finish all tasks (minutes):  min={min_best_score}   max={max_best_score}   average={average_best_score}")

    
dict_pso["y_values"] = [(val / runs) for val in dict_pso["y_values"]]

plt.plot(dict_pso["x_values"], dict_pso["y_values"], linewidth = 2.0, color = 'green')
plt.title("Particle Swarm Optimization's Average (best so far) Fitness")
plt.xlabel("Number of Iterations")
plt.ylabel("Best Fitness")
plt.show()