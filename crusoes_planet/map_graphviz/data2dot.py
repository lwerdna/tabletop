#!/usr/bin/env python


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
			paths[path_cur].append(line.split(',')[1:])

		else:
			path_cur = line.split(',')[0]
			assert not path_cur in paths
			paths[path_cur] = []

	return paths

if __name__ == '__main__':
	data = read_data()

	print('digraph map {')
	print('\tratio="fill";')
	print('\tsize="22,17!"')
	print('\tmargin=0;')

	for path_name in data:
		print('\tCrashSite -> %s' % path_name)
		prev = path_name
		for (i, path_data) in enumerate(data[path_name]):
			node_name = '%s%d' % (path_name, i)
			print('\t%s -> %s' % (prev, node_name))
			prev = node_name
		print('\t%s -> Market' % prev)

	print('}')
