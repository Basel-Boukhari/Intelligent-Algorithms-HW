import random
import matplotlib.pyplot as plt

#دالة تولد بيانات تجريبية وقت انجاز كل موظف للمهمة
def generate_sample(tasks_number, employees_number, seed=None):
    min_time = 5  #اقل وقت لتنفيذ المهمة بالدقائق 
    max_time = 10 * 60  #اعلى وقت لتنفيذ المهمة 
    #seed خيار اضفته يساعدني بالتجارب 
    rng = random.Random(seed)  #لتوليد المصفوفة نفسها عند المقارنة 

    t = [
        [rng.randint(min_time, max_time) for _ in range(tasks_number)]
        for _ in range(employees_number)
    ]
    return t

#دالة توزيع واحد (كم يستغرق التوزيع لحتى ينتهي اخر موظف من مهامه )
def fitness_calculation(tasks_number, employees_number, t, individual):
    load = [0] * employees_number

    for task in range(tasks_number):
        employee = individual[task]
        load[employee] += t[employee][task]

    return max(load)

#(العجلة الروليتية) اختيار موظف عشوائي بحسب الاوزان
def choose_employee(probabilities):
    total = sum(probabilities)
    value = random.random() * total
    current = 0

    for employee in range(len(probabilities)):
        current += probabilities[employee]
        if value <= current:
            return employee

    return len(probabilities) - 1
# بناء توزيع كامل للمهام بواسطة نملة واحدة تعتمد على الفيرومون ووقت الإنجاز المتوقع
def create_ant_solution(
    tasks_number,
    employees_number,
    t,
    pheromone,
    alpha,
    beta
):
    # مصفوفة لحفظ الموظف المسؤول عن كل مهمة
    solution = [-1] * tasks_number

    # مصفوفة لحفظ عبء العمل الحالي لكل موظف
    loads = [0] * employees_number

    # إنشاء قائمة المهام وخلطها عشوائياً
    task_indices = list(range(tasks_number))
    random.shuffle(task_indices)

    # المرور على جميع المهام
    for task_id in task_indices:

        # تخزين أوزان اختيار كل موظف للمهمة الحالية
        weights = []

        # معرفة أكبر عبء عمل حالي
        current_max_load = max(loads)

        # حساب وزن كل موظف للمهمة الحالية
        for emp_id in range(employees_number):

            # العبء المتوقع إذا أُسندت المهمة لهذا الموظف
            predicted_load = loads[emp_id] + t[emp_id][task_id]
            expected_makespan = max(
                current_max_load,
                predicted_load
            )

            # كلما كان وقت الإنجاز المتوقع أقل زادت جاذبية اختيار الموظف
            attractiveness = 1 / max(expected_makespan, 1)

            # تأثير الفيرومون
            pheromone_effect = (
                pheromone[emp_id][task_id] ** alpha
            )
            heuristic_effect = (
                attractiveness ** beta
            )

            # حساب الوزن النهائي للموظف
            weights.append(
                pheromone_effect * heuristic_effect
            )
        selected_emp = choose_employee(weights)
        solution[task_id] = selected_emp
        loads[selected_emp] += t[selected_emp][task_id]

    return solution
    
def ant_colony_algorithm(
    tasks_number,
    employees_number,
    t,
    ant_count,
    max_iteration,
    alpha,
    beta,
    evaporation_rate,
    Q
):
    # تهيئة مصفوفة الفيرومون بقيمة ابتدائية
    pheromone_matrix = [
        [1.0] * tasks_number
        for _ in range(employees_number)
    ]

    # أفضل حل تم إيجاده
    global_best_solution = None
    global_best_score = float("inf")

    # لتخزين بيانات الرسم البياني
    best_scores = []
    iterations = []
    for current_iteration in range(max_iteration):
        solutions = []

        # إنشاء حلول بواسطة جميع النمل
        for _ in range(ant_count):
            solution = create_ant_solution(
                tasks_number,
                employees_number,
                t,
                pheromone_matrix,
                alpha,
                beta
            )

            fitness = fitness_calculation(
                tasks_number,
                employees_number,
                t,
                solution
            )

            solutions.append((fitness, solution))

        # استخراج أفضل حل في هذا التكرار
        current_best_score, current_best_solution = min(
            solutions,
            key=lambda x: x[0]
        )
        if current_best_score < global_best_score:
            global_best_score = current_best_score
            global_best_solution = current_best_solution.copy()

        # تبخير الفيرومون
        for emp in range(employees_number):
            for task in range(tasks_number):
                pheromone_matrix[emp][task] *= (
                    1 - evaporation_rate
                )
        # حساب كمية الفيرومون المضافة
        pheromone_amount = Q / max(
            current_best_score,
            1
        )
        # إضافة الفيرومون إلى إسنادات أفضل حل في هذا التكرار
        for task in range(tasks_number):
            assigned_employee = current_best_solution[task]

            pheromone_matrix[
                assigned_employee
            ][task] += pheromone_amount
        best_scores.append(global_best_score)
        iterations.append(current_iteration)

    return (
        global_best_score,
        global_best_solution,
        best_scores,
        iterations
    )
m = int(input("How many tasks are there? "))
n = int(input("How many employees are there? "))

ant_count = 50
max_iteration = 30
alpha = 1.0
beta = 2.0
evaporation_rate = 0.1
Q = 100.0
# seed لحتى اولد مصفوفة الاوقات نفسها استخدم نفس ال 
t = generate_sample(m, n, seed=42)
best_score, best_solution, best_scores, iterations = ant_colony_algorithm(
    m,
    n,
    t,
    ant_count,
    max_iteration,
    alpha,
    beta,
    evaporation_rate,
    Q
)

print("Best assignment:", best_solution)
print("Best makespan:", best_score, "minutes")

plt.plot(iterations, best_scores, marker="o")
plt.xlabel("Iteration")
plt.ylabel("Best Makespan (minutes)")
plt.title("Ant Colony Optimization")
plt.show()
