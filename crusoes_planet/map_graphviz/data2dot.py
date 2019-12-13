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
	data = read_data()

	print('digraph map {')
	#print('\tratio="fill";')
	#print('\tsize="11,8.5!"')
	print('\tsize="11,8";')
	print('\trankdir="LR";')
	print('\tmargin=0;')

	# do a pass to define the node properties
	for path_name in data:
		stops = data[path_name]

		for i in range(len(stops)):
			stop_name = '%s%d' % (path_name, i)
			print('\t%s' % stop_name)
			print('\t[')
			print('\t\tshape = none,')
			print('\t\theight = 1,')
			print('\t\twidth = 1,')

			html = '<table border="1" cellspacing="0">'
			stop_data = stops[i]
			[banana,egg,water,spfish,apple,diamond,leisure,spear,fish,grapes,cb,mil,t40] = stop_data

			if list(filter(lambda x: x != 0, stop_data)) == []:
				sys.stderr.write(str(stop_data))
				html += '<tr><td>        </td></tr>'

			if False:
				if apple:
					html += '<tr><td bgcolor="#CD5C5C">%d apple</td></tr>' % apple
				if banana:
					html += '<tr><td bgcolor="#FFFACD">%d banana</td></tr>' % banana
				if grapes:
					html += '<tr><td bgcolor="#9370DB">%d grapes</td></tr>' % grapes
				if egg:
					html += '<tr><td>%d egg</td></tr>' % egg
				if water:
					html += '<tr><td bgcolor="#AFEEEE">%d water</td></tr>' % water
				if spfish:
					html += '<tr><td bgcolor="#98FB98">%d (sp)fish</td></tr>' % spfish
				if diamond:
					html += '<tr><td>%d diamond</td></tr>' % diamond
				if leisure:
					html += '<tr><td bgcolor="#FFC0CB">%d leisure</td></tr>' % leisure
				if spear:
					html += '<tr><td bgcolor="#ECD9B0">%d spear</td></tr>' % spear
				if fish:
					html += '<tr><td bgcolor="#98FB98">%d fish</td></tr>' % fish
				if cb:
					html += '<tr><td bgcolor="#C0C0C0">%d cb</td></tr>' % cb
				if mil:
					html += '<tr><td bgcolor="#C0C0C0">%d mil</td></tr>' % mil
				if t40:
					html += '<tr><td bgcolor="#C0C0C0">%d t40</td></tr>' % t40
			else:
				html += '<tr><td bgcolor="#CD5C5C">apple</td></tr>' * apple
				html += '<tr><td bgcolor="#FFFACD">banana</td></tr>' * banana
				html += '<tr><td bgcolor="#9370DB">grapes</td></tr>' * grapes
				html += '<tr><td>egg</td></tr>' * egg
				html += '<tr><td bgcolor="#AFEEEE">water</td></tr>' * water
				html += '<tr><td bgcolor="#98FB98">(sp)fish</td></tr>' * spfish
				html += '<tr><td>diamond</td></tr>' * diamond
				html += '<tr><td bgcolor="#FFC0CB">leisure</td></tr>' * leisure
				html += '<tr><td bgcolor="#ECD9B0">spear</td></tr>' * spear
				html += '<tr><td bgcolor="#98FB98">fish</td></tr>' * fish
				html += '<tr><td bgcolor="#C0C0C0">cb</td></tr>' * cb
				html += '<tr><td bgcolor="#C0C0C0">mil</td></tr>' * mil
				html += '<tr><td bgcolor="#C0C0C0">t40</td></tr>' * t40
			html += '</table>'

			print('\t\tlabel=<%s>' % html)
			print('\t]')

	for path_name in data:
		print('\tCrashSite -> %s' % path_name)
		prev = path_name
		for (i, path_data) in enumerate(data[path_name]):
			node_name = '%s%d' % (path_name, i)
			print('\t%s -> %s' % (prev, node_name))
			prev = node_name
		print('\t%s -> Market' % prev)

	print('}')
