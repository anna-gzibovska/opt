import random
import time as time_lib

class Question:
    def __init__(self, value, time):
        self.value = value
        self.time = time


def init_solution(questions, max_time):
    question_list = []
    
    random_index = list(range(len(questions)))
    random.shuffle(random_index)

    for index in random_index:
        question = questions[index]
        if max_time - question.time >= 0:
            question_list.append(index)
            max_time -= question.time

    return question_list


def sum_solution(questions, selected):
    solution_time = sum([question.time for i, question in enumerate(questions) if i in selected])
    solution_val = sum([question.value for i, question in enumerate(questions) if i in selected])

    return solution_time, solution_val


def evaluate(questions, old_solution, new_solution):
    t1, v1 = sum_solution(questions, old_solution)
    t2, v2 = sum_solution(questions, new_solution)

    if v2 > v1 or (v2 == v1 and t2 < t1):
        return new_solution
    return old_solution
    

def generate(questions, current_solution, max_time):
    new_solution = current_solution[:]
    solution_time, solution_val = sum_solution(questions, current_solution)
    index = 0
    while index != len(questions):
        cur_time = 0
        if index in current_solution:
            cur_time = questions[index].time
            if index in new_solution:
                new_solution.remove(index)
        random_index = random.randint(0, len(questions) - 1)
        if random_index not in new_solution and questions[random_index].time + solution_time - cur_time <= max_time:
            new_solution.append(random_index)
            solution_time += questions[random_index].time
            break
        elif random_index in new_solution:
            new_solution.remove(random_index)
        else:
            to_remove = current_solution[random.randint(0, len(current_solution) - 1)]
            if to_remove in new_solution:
                new_solution.remove(to_remove)

        index += 1
    return new_solution


def lahc(questions, time, max_attempts, n):
    solution_exists = [question.time for question in questions if question.time <= time]
    if not solution_exists:
        return [], (0, time)
    
    
    current_solution = init_solution(questions, time)
    history = [current_solution]
    k = 0
    no_progress = 0
    while max_attempts:
        k = k % n
        new_solution = generate(questions, current_solution, time)

        best_solution = evaluate(questions, current_solution, new_solution)
        if best_solution != current_solution:
            current_solution = best_solution
            no_progress = 0
        else:
            best_solution = evaluate(questions, history[k], new_solution)
            if best_solution == new_solution:
                current_solution = new_solution
                no_progress = 0
            else:
                no_progress += 1
                
        if no_progress >= 100:
            current_solution = init_solution(questions, time)

        history.append(current_solution)

        max_attempts -= 1
        k += 1

        if len(history) > n:
            history.pop(0)

    return current_solution, sum_solution(questions, current_solution)


def test_solution(n, x, v, t):
    questions = [Question(val, time) for val, time in zip(v, t)]
    start = time_lib.time()
    solution, res = lahc(questions, x, 1000, n)

    return solution, res, time_lib.time() - start



#N X V T selected_indices total_grade total_time
#1
n = 5
x = 110
v = [10, 20, 5, 15, 20]
t = [20, 35, 15, 20, 30]
solution, grade, time = test_solution(n, x, v, t)
print(n, x, v, t, solution, grade, time)
#2
n = 4
x = 30
v = [30, 10, 10, 10]
t = [30, 10, 10, 10]
solution, grade, time = test_solution(n, x, v, t)
print(n, x, v, t, solution, grade, time)
#3
n = 6
x = 75
v = [5, 10, 20, 20, 30, 15]
t = [10, 15, 20, 20, 26, 18]
solution, grade, time = test_solution(n, x, v, t)
print(n, x, v, t, solution, grade, time)
#4
n = 10
x = 130
v = [2, 10, 20, 40, 15, 5, 5, 15, 30, 20]
t = [3, 10, 20, 40, 15, 5, 6, 15, 30, 20]
solution, grade, time = test_solution(n, x, v, t)
print(n, x, v, t, solution, grade, time)
#5
n = 15
x = 500
v = [40, 20, 10, 10, 5, 8, 4, 24, 16, 15, 20, 30, 35, 12, 45]
t = [60, 30, 20, 15, 2, 5, 2, 18, 16, 15, 21, 29, 34, 13, 70]
solution, grade, time = test_solution(n, x, v, t)
print(n, x, v, t, solution, grade, time)
#6
n = 4
x = 20
v = [20, 15, 30, 40]
t = [25, 22, 29, 35]
solution, grade, time = test_solution(n, x, v, t)
print(n, x, v, t, solution, grade, time)
#7
n = 8
x = 150
v = [30, 20, 40, 15, 10, 25, 35, 45]
t = [50, 30, 60, 20, 10, 35, 40, 55]
solution, grade, time = test_solution(n, x, v, t)
print(n, x, v, t, solution, grade, time)
