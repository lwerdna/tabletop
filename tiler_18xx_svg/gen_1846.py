#!/usr/bin/env python

import re
import os
import sys

import xml.etree.ElementTree as ET

# open an file and shift it +x +y
def shift(fpath, x, y):
	#print 'opening file: %s' % fpath
	tree = ET.parse(fpath)
	root = tree.getroot()

	for child in root:
		# incoming tags are like "{http://www.w3.org/2000/svg}ellipse"
		# remove that initial nonsense
		m = re.match(r'^({.*})?([a-zA-Z]+)$', child.tag)
		(dummy,tag) = m.group(1,2)
		assert m
		if tag == 'path':
			tmp = []
			cmds = child.get('d')
			while cmds:
				if cmds.startswith(' '):
					cmds = cmds[1:]
				elif cmds[0:2] in ('M ', 'L '):
					m = re.match(r'(.) (\d+),(\d+)', cmds)
					assert(m)
					tmp.append('%s %d %d' % (m.group(1), int(m.group(2))+x, int(m.group(3))+y))
					cmds = cmds[len(m.group(0)):]
				elif cmds[0:2] in ('A '):
					m = re.match(r'(. \d+,\d+ \d+ \d+,\d+ )(\d+),(\d+)', cmds)
					assert(m)
					tmp.append('%s %d,%d' % (m.group(1), int(m.group(2))+x, int(m.group(3))+y))
					cmds = cmds[len(m.group(0)):]
				elif cmds[0] == 'Z':
					tmp.append('Z')
					cmds = cmds[1:]
				else:
					raise Exception("unrecognized cmds in path: " + cmds)
			child.set('d', ' '.join(tmp))
		elif tag in ['circle', 'ellipse']:
			child.set('cx', str(int(child.get('cx'))+x))
			child.set('cy', str(int(child.get('cy'))+y))
		elif tag in ['text']:
			child.set('x', str(int(child.get('x'))+x))
			child.set('y', str(int(child.get('y'))+y))			
		else:
			raise Exception("oh no, dunno what to do with: " + child.tag)

	tmp = ET.tostring(root)
	tmp = re.sub(r'<svg.*?>', '', tmp)
	tmp = tmp.replace('</svg>', '')
	return tmp

def make_page(width, height, positions, tiles, fname):
	result = ''
	result += '<?xml version="1.0"?>\n'
	result += '<svg width="%d" height="%d" xmlns="http://www.w3.org/2000/svg" version="1.1">\n' % \
		(width, height)

	print 'tile: ', tiles

	while len(tiles) < len(positions):
		tiles.append('tile-blank.svg')

	for (i,position) in enumerate(positions):
		fpath = os.path.join('.', 'tiles', tiles[i])
		print 'fpath: %s' % fpath
		result += '\n<!-- inserting file %s -->\n' % fpath
		result += shift(fpath, position[0], position[1])

	result += '</svg>\n'

	print 'writing ' + fname
	with open(fname, 'w') as fp:
		fp.write(result)

if __name__ == '__main__':
	ET.register_namespace('', 'http://www.w3.org/2000/svg')

	(hex_count_x, hex_count_y) = (7,5)
	(hex_width, hex_height) = (392, 340)
	(page_width, page_height) = (2486, 1920)

	#print shift('./tiles/tile-5.svg', 0, 0)
	#sys.exit(0)

	margin_n = 110
	margin_e = 67
	positions = []
	for i in range(6):
		positions.append([margin_e + i*hex_width, margin_n + 0])
	for i in range(5):
		positions.append([margin_e + hex_width/2 + i*hex_width, margin_n + hex_height])
	for i in range(6):
		positions.append([margin_e + i*hex_width, margin_n + 2*hex_height])
	for i in range(5):
		positions.append([margin_e + hex_width/2 + i*hex_width, margin_n + 3*hex_height])
	for i in range(6):
		positions.append([margin_e + i*hex_width, margin_n + 4*hex_height])

	pageNum = 0
	# blank test page
	make_page(page_width, page_height, positions, [], 'sheet_%02d.svg' % pageNum)
	pageNum += 1
	# yellow pages
	yellows = ['tile5.svg']*3 + ['tile6.svg']*4 + ['tile7.svg']*5 + ['tile8.svg']*16 + ['tile9.svg']*16 + ['tile57.svg']*4 + ['tile291.svg'] + ['tile292.svg'] + ['tile293.svg']

	while yellows:
		make_page(page_width, page_height, positions, yellows[0:28], 'sheet_%02d.svg' % pageNum)
		yellows = yellows[28:]
		pageNum += 1
	
