#!/usr/bin/env python

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

def removed_all_modifiers():
	""" return how many removed for every modifier combination """
	return [removed(3, 0), removed(2, 0), removed(1, 0), removed(0, 0),
			removed(0, 1), removed(0, 2), removed(0, 3)]

def sum_lists(a, b):
	""" add respective elements from two lists """
	return list(map(sum, list(zip(a, b))))

result1 = [0]*7
result2 = [0]*7
result3 = [0]*7
result4 = [0]*7

N_TRIALS = 1000000

for trials in range(N_TRIALS):
	data = removed_all_modifiers()
	result1 = sum_lists(result1, data)
	result2 = sum_lists(result2, data)
	result3 = sum_lists(result3, data)
	result4 = sum_lists(result4, data)

	data = removed_all_modifiers()
	result2 = sum_lists(result2, data)
	result3 = sum_lists(result3, data)
	result4 = sum_lists(result4, data)

	data = removed_all_modifiers()
	result3 = sum_lists(result3, data)
	result4 = sum_lists(result4, data)

	data = removed_all_modifiers()
	result4 = sum_lists(result4, data)

for i in range(7):
	result1[i] /= N_TRIALS
	result2[i] /= N_TRIALS
	result3[i] /= N_TRIALS
	result4[i] /= N_TRIALS

print(result1)
print(result2)
print(result3)
print(result4)
