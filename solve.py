import requests
from numpy import argsort
from multiprocessing import Pool
import random
import json
import time

# Need for time check (uncoment last 2 lines to see how long the program will run)
start = time.time()

# Number of questions
n = 25
# Number of question option
m = 4
url = 'https://tlgrm.info/test/'
header =  {"Content-Type": "application/json"}


def get_right_answer(answer_list):
    # answer_list - type(list) -> list of answers to check
    # result - type(int) -> number of right answers

    body = {'answers': answer_list}
    r = requests.post(url, headers=header, json=body)
    result =r.json().get('right_answers', -1)
    return result


def multiprocess_calc(var_list, func=get_right_answer, processes=25):
    # var_list - type(list(list)) -> list of answers to check
    # result - type(list) -> return list of correct answers

    p = Pool(processes=processes)
    result = p.map(func, var_list)
    p.close()
    return result


# Generate a sequence that contains the correct answers, but are put in a random order
all_opt_amount = multiprocess_calc([[i] * n for i in range(m)])
ans_list = [i for i, opt_amount in enumerate(all_opt_amount) for _ in range(opt_amount) ]
random.shuffle(ans_list)


# Create sorted pool of all options (list items must only be int)
options_pool = [int(i) for i in argsort(all_opt_amount)[::-1]]

# List of questions that shows whether we know correct answer or don't(all are False for now)
is_correct = [False for i in range(n)]
# List of lists that shows what option are incorrect for each question
is_not_option = [[] for i in range(n)]

for _ in range(m):
    # Check if we know all correct answers if we do we can quit
    if sum(is_correct) == n:
        break

    list_of_change = [] # List of tuples that show how options was changed ex.(1 -> 3)
    pool_to_check = [ans_list.copy()] # Pool that will be checked for right answers
    temp_ans_list = ans_list.copy() # list of answers copy

    for pos, cur_opt in enumerate(temp_ans_list):
        # If we already know the answer we can pass this iteration
        if is_correct[pos]:
            continue

        # We need to pick an option that we haven't checked yet
        idx = 0
        wrong_opts = [cur_opt] + is_not_option[pos]
        while options_pool[idx] in wrong_opts: idx += 1

        # Assigning new option, update pool_to_check & list_of_change
        new_opt = options_pool[idx]
        temp_ans_list[pos] = new_opt
        pool_to_check.append(temp_ans_list.copy())
        list_of_change.append((cur_opt, new_opt))

    # Get list of correct answers
    feedback = multiprocess_calc(pool_to_check)

    # Now we can say which questions were correct, or which become correct, or which are incorrect
    # We have 3 possible states:
    # 1. After the change we get bigger right answers -> changed option was correct
    # 2. After the change we get equal amount of right answers -> both options are incorrect
    # 3. After the change we get less right answers -> previous option was correct
    idx = 0 # Counter for feedback and list_of_change
    for i in range(n):
        if not is_correct[i]:
            # 1
            if feedback[idx+1] > feedback[idx]:
                ans_list[i] = list_of_change[idx][1]
                is_correct[i] = True
            # 3
            elif feedback[idx+1] < feedback[idx]:
                ans_list[i] = list_of_change[idx][0]
                is_correct[i] = True
            # 2
            else:
                is_not_option[i] += [list_of_change[idx][1], list_of_change[idx][0]]
            idx += 1

# Print result
print('The correct answers are: ', ans_list)

# For last check :)
print(f'{n} / {get_right_answer(ans_list)} answers are correct!')

# Needed for time check
# end = time.time()
# print(f'Program was running = {round(end - start, 2)} sec.')

