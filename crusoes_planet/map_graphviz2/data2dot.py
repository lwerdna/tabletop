#!/usr/bin/env python

import sys

def read_data():
	with open('data.csv') as fp:
		lines = fp.readlines()

	paths = {}
	path_cur = ''
	for line in map(lambda x: x.strip(), lines):
		if line == '':
			continue

		if line[0].isdigit():
			assert path_cur
			assert path_cur in paths
			values = list(map(int, line.split(',')[1:]))
			paths[path_cur].append(values)

		else:
			path_cur = line.split(',')[0]
			assert not path_cur in paths
			paths[path_cur] = []

	return paths

if __name__ == '__main__':
	incrementer = 0

	data = read_data()

	print('digraph map {')
	#print('\tratio="fill";')
	#print('\tsize="11,8.5!"')
	#print('\tsize="11,8";')
	print('\tcompound=true;')
	print('\trankdir="LR";')
	print('\tmargin=0;')

	# do a pass to define the subgraphs
	for path_name in data:
		stops = data[path_name]

		for i in range(len(stops)):
			stop_name = '%s%d' % (path_name, i)
			print('\tsubgraph cluster_%s' % stop_name)
			print('\t{')
			#print('\t\tstyle=filled;')
			#print('\t\tcolor=lightgrey;')

			if i == 0:
				print('\tlabel = "%s";' % path_name)

			stop_data = stops[i]
			[banana,egg,water,spfish,apple,diamond,leisure,spear,fish,grapes,cb,mil,t40] = stop_data
				
			print('\t\t%s_entry [ style = invis ];' % stop_name)

			for i in range(apple):
				print('\t\tnode%d [ label = "apple", style="filled", color="pink" ];' % incrementer)
				incrementer += 1
			for i in range(banana):
				print('\t\tnode%d [ label = "banana", style="filled", color="yellow" ];' % incrementer)
				incrementer += 1
			for i in range(water):
				print('\t\tnode%d [ label = "water", style="filled", color="blue" ];' % incrementer)
				incrementer += 1
			for i in range(egg):
				print('\t\tnode%d [ label = "egg", style="filled", color="white" ];' % incrementer)
				incrementer += 1
			for i in range(spfish):
				print('\t\tnode%d [ label = "spfish", style="filled", color="green" ];' % incrementer)
				incrementer += 1
			for i in range(fish):
				print('\t\tnode%d [ label = "fish", style="filled", color="green" ];' % incrementer)
				incrementer += 1
#			for i in range(diamond):
#				print('\t\tnode%d [ label = "diamond", style="filled", color="white", shape="diamond" ];' % incrementer)
#				incrementer += 1
#			for i in range(leisure):
#				print('\t\tnode%d [ label = "leisure", style="filled", color="purple" ];' % incrementer)
#				incrementer += 1
#			for i in range(spear):
#				print('\t\tnode%d [ label = "spear", style="filled", color="brown" ];' % incrementer)
#				incrementer += 1
#			for i in range(grapes):
#				print('\t\tnode%d [ label = "grapes", style="filled", color="purple" ];' % incrementer)
#				incrementer += 1
#			for i in range(cb):
#				print('\t\tnode%d [ label = "cb", style="filled", color="gray" ];' % incrementer)
#				incrementer += 1
#			for i in range(mil):
#				print('\t\tnode%d [ label = "mil", style="filled", color="gray" ];' % incrementer)
#				incrementer += 1
#			for i in range(t40):
#				print('\t\tnode%d [ label = "t40", style="filled", color="gray" ];' % incrementer)
#				incrementer += 1

			print('\t\t%s_exit [ style = invis ];' % stop_name)
			print('\t}')

	# do another pass to connect the subgraphs
	for path_name in data:
		path_len = len(data[path_name])

		print('\tCrashSite -> %s0_entry [lhead = cluster_%s0]' % (path_name, path_name))

		for i in range(path_len-1):
			A = '%s%d_exit' % (path_name, i)
			B = '%s%d_entry' % (path_name, i+1)
			Aclus = 'cluster_%s%d' % (path_name, i)
			Bclus = 'cluster_%s%d' % (path_name, i+1)
			print('\t%s -> %s [ltail=%s, lhead=%s]' % (A, B, Aclus, Bclus))

		print('\t%s%d_exit -> Market [ltail = cluster_%s%d]' % (path_name, path_len-1, path_name, path_len-1))

	print('}')
