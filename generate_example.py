import random

n = 4

for _ in range(10):
    #m = random.randint(5,20)
    #m = random.randint(21,1000)
    #m = random.randint(1001, 10000)
    def generate_sample(tasks_number, employees_number):
        min_time=5
        max_time=40*60

        t=[[random.randint(min_time, max_time) for i in range(tasks_number)] for j in range(employees_number)]
        print(t)

        return t

    t=generate_sample(m,n)
   

    lines = [[n,m]]
    for i in range(n):
        lines.append(t[i])
    lines=str(lines)

    if m>=5 and m<=20:
        file_name = f"small_test{_+1}.txt"
    elif m>=20 and m<=1000:
        file_name = f"medium_test{_+1}.txt"
    elif m>=1001 and m<=10000:
        file_name = f"large_test{_+1}.txt"

    f = open(file_name,"w")
    f.writelines(lines)