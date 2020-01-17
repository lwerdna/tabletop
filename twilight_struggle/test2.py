#!/usr/bin/env python

import sys
import random

def roll(modifier=0):
	""" return a dice roll, with modifier """
	return random.randint(1,6) + modifier

def rolldiff(modifier_a=0, modifier_b=0):
	""" return difference between two dice rolls, given modifiers """
	return roll(modifier_a) - roll(modifier_b)

def removed(modifier_a=0, modifier_b=0):
	""" return how many influence removed """
	diff = rolldiff(modifier_a, modifier_b)
	return 0 if diff <= 0 else diff

def success(modifier_a, modifier_b, goal):
	""" return True/False depending on if a roll removed a target amount """
	return removed(modifier_a, modifier_b) >= goal

def removed_all_modifiers():
	""" return how many removed for every modifier combination """
	return [removed(3, 0), removed(2, 0), removed(1, 0), removed(0, 0),
			removed(0, 1), removed(0, 2), removed(0, 3)]

def success_all_modifiers(goal):
	return [success(3, 0, goal), success(2, 0, goal), success(1, 0, goal),
			success(0, 0, goal), success(0, 1, goal), success(0, 2, goal),
			success(0, 3, goal)]

def sum_lists(a, b):
	""" add respective elements from two lists """
	return list(map(sum, list(zip(a, b))))

def sum_lists_success(a, b):
	""" add respective SUCCESS elements from two lists """
	return map(lambda x: int(bool(x)), sum_lists(a, b))

result1 = [0]*7
result2 = [0]*7
result3 = [0]*7
result4 = [0]*7

N_TRIALS = 100000
GOAL = 1
if(sys.argv[1:]):
	GOAL = int(sys.argv[1])

for trials in range(N_TRIALS):
	tmp1 = [0]*7
	tmp2 = [0]*7
	tmp3 = [0]*7
	tmp4 = [0]*7

	data = success_all_modifiers(GOAL)
	tmp1 = sum_lists_success(tmp1, data)
	tmp2 = sum_lists_success(tmp2, data)
	tmp3 = sum_lists_success(tmp3, data)
	tmp4 = sum_lists_success(tmp4, data)

	data = success_all_modifiers(GOAL)
	tmp2 = sum_lists_success(tmp2, data)
	tmp3 = sum_lists_success(tmp3, data)
	tmp4 = sum_lists_success(tmp4, data)

	data = success_all_modifiers(GOAL)
	tmp3 = sum_lists_success(tmp3, data)
	tmp4 = sum_lists_success(tmp4, data)

	data = success_all_modifiers(GOAL)
	tmp4 = sum_lists_success(tmp4, data)

	result1 = sum_lists(result1, tmp1)
	result2 = sum_lists(result2, tmp2)
	result3 = sum_lists(result3, tmp3)
	result4 = sum_lists(result4, tmp4)

for i in range(7):
	result1[i] = result1[i]*100/N_TRIALS
	result2[i] = result2[i]*100/N_TRIALS
	result3[i] = result3[i]*100/N_TRIALS
	result4[i] = result4[i]*100/N_TRIALS

print('| 1 | ' + ' | '.join(map(str, result1)) + '|')
print('| 2 | ' + ' | '.join(map(str, result2)) + '|')
print('| 3 | ' + ' | '.join(map(str, result3)) + '|')
print('| 4 | ' + ' | '.join(map(str, result4)) + '|')

