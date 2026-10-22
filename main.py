import matplotlib.pyplot as plt

import genetic_algorithm as GA, ant_colony_algorithm as ACO, swarm_algorithm as PSO

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
                "(It will add another run for memory monitoring): "))
t, m, n = read_test(file_name)

f = open(f"{file_name}_results.txt", 'w')
f.close()

dict_algos_funcs = {"GA": GA.run_ga, "PSO": PSO.run_pso, "ACO": ACO.run_aco}
dict_algos_colors = {"GA": "blue", "PSO":"green", "ACO":"red"}
dict_results = {}

line = ""
for j in range(40):
    line += "-"

for algorithm, function in dict_algos_funcs.items():
    
    print(line)
    print(f"Running {algorithm}")
    print(line)
    dict_results[algorithm] = function(t, m, n, runs)

    f = open(f"{algorithm.lower()}_best_solution_for_{file_name}.txt", 'w')
    f.write(str(dict_results[algorithm]["best_solution"]))
    f.close()    

    file_lines = []
    file_lines.append(line + '\n')
    file_lines.append(algorithm + '\n')
    file_lines.append(line + '\n')

    max_time = round(max(dict_results[algorithm]["times"]),4)
    min_time = round(min(dict_results[algorithm]["times"]),4)
    average_time = round(sum(dict_results[algorithm]["times"]) / len(dict_results[algorithm]["times"]),4)
    s = f"Time (seconds):  min={min_time}   max={max_time}   average={average_time}\n"
    print(s)
    file_lines.append(s)

    max_memory = round(max(dict_results[algorithm]["memories"]),4)
    min_memory = round(min(dict_results[algorithm]["memories"]),4)
    average_memory = round(sum(dict_results[algorithm]["memories"]) / len(dict_results[algorithm]["memories"]),4)
    s = f"Memory (MB):  min={min_memory}   max={max_memory}   average={average_memory}\n"
    print(s)
    file_lines.append(s)

    max_memory_time = round(max(dict_results[algorithm]["memory_times"]),4)
    min_memory_time = round(min(dict_results[algorithm]["memory_times"]),4)
    average_memory_time = round(sum(dict_results[algorithm]["memory_times"])/len(dict_results[algorithm]["memory_times"]),4)
    s = f"Time taken with memory measuring (second):  min={min_memory_time}   max={max_memory_time}   average={average_memory_time}\n"
    print(s)
    file_lines.append(s)
    max_best_score = round(max(dict_results[algorithm]["best_scores"]),4)
    min_best_score = round(min(dict_results[algorithm]["best_scores"]),4)
    average_best_score = round(sum(dict_results[algorithm]["best_scores"]) / len(dict_results[algorithm]["best_scores"]),4)
    s = f"Time to Finish all tasks (minutes):  min={min_best_score}   max={max_best_score}   average={average_best_score}\n"
    print(s)
    file_lines.append(s)

    f = open(f"{file_name}_results.txt", 'a')
    f.writelines(file_lines)
    f.close()


for algorithm, color in dict_algos_colors.items():
    plt.plot(dict_results[algorithm]["x_values"], dict_results[algorithm]["y_values"],
             linewidth = 2.0, color = color, label = algorithm)

plt.title(f"Algorithms Comparison on {file_name} (Average (best so far) Fitness over {runs} runs)")
plt.xlabel("Number of Iterations")
plt.ylabel("Best Fitness")
plt.legend()
plt.show()



