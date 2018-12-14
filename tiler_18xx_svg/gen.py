#!/usr/bin/env python

import re
import os
import sys

import xml.etree.ElementTree as ET

# shift svg +x +y
def svg_shift(data, x, y):
	root = ET.fromstring(data)

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
				# [M]ove absolute: we shift
				elif cmds[0:2] in ('M ', 'L '):
					m = re.match(r'(.) ([\d\.]+),([\d\.]+)', cmds)
					assert(m)
					tmp.append('%s %f %f' % (m.group(1), float(m.group(2))+x, float(m.group(3))+y))
					cmds = cmds[len(m.group(0)):]
				# [m]ove relative: we NOP
				elif cmds[0:2] in ('m '):
					m = re.match(r'(.) ([\d\.]+),([\d\.]+)', cmds)
					assert(m)
					tmp.append(cmds[0:len(m.group(0))])
					cmds = cmds[len(m.group(0)):]
				# [A]rc absolute: we shift
				elif cmds[0:2] in ('A '):
					strlen = re.match(r'A [\d\., ]+', cmds).end()
					substr = cmds[0:strlen]
					numbers = map(float, re.findall(r'[\d\.]+', substr))
					numbers[5] += x
					numbers[6] += y
					assert len(numbers) == 7
					tmp.append('A %f,%f %f %d,%d %f,%f' % tuple(numbers))
					cmds = cmds[strlen:]
				# [A]rc relative, we NOP
				elif cmds[0:2] in ('a '):
					strlen = len(re.match(r'a [-\d\., ]+', cmds).group(0))
					tmp.append(cmds[0:strlen])
					cmds = cmds[strlen:]
				# Z is close path
				elif cmds[0] in ('Z','z'):
					tmp.append('Z')
					cmds = cmds[1:]
				else:
					raise Exception("unrecognized cmds in path: " + cmds)
			child.set('d', ' '.join(tmp))
		elif tag in ['circle', 'ellipse']:
			child.set('cx', str(int(child.get('cx'))+x))
			child.set('cy', str(int(child.get('cy'))+y))
		elif tag in ['text']:
			child.set('x', str(float(child.get('x'))+x))
			child.set('y', str(float(child.get('y'))+y))
		elif tag in ['line']:
			child.set('x1', str(float(child.get('x1'))+x))
			child.set('y1', str(float(child.get('y1'))+y))
			child.set('x2', str(float(child.get('x2'))+x))
			child.set('y2', str(float(child.get('y2'))+y))
		elif tag in ['polygon']:
			tmp = []
			for pts in child.get('points').split(' '):
				(x_,y_) = map(int, re.match(r'(\d+),(\d+)', pts).group(1,2))
				tmp.append('%d,%d' % (x_+x, y_+y))
			child.set('points', ' '.join(tmp))
		elif tag in ['metadata', 'defs', 'namedview']:
			pass
		else:
			raise Exception("oh no, dunno what to do with: " + child.tag)

	tmp = ET.tostring(root)
	tmp = tmp.replace('.000000', '')
	return tmp

def tile_get_bleed(data):
	regex = r'(<path d=" ?[MLZ\d\., ]+" fill="([^"]+)" stroke="[^"]+" (?:stroke-width="1" stroke-linejoin="round"|stroke-linejoin="round" stroke-width="1") ?/>)'
	m = re.search(regex, data, re.DOTALL)
	if not m:
		raise Exception("couldn't find initial tile outliner")
	(tmp, fill) = m.group(1,2)
	if fill=='none':
		return ''
	tmp = tmp.replace('stroke-width="1"', 'stroke-width="16"')
	tmp = tmp.replace('stroke="#00000000"', 'stroke="%s"' % fill)
	return tmp

def svg_dot_outline(data):
	regex = r'<path d="[MLZ\d\. ]+?" fill="none" stroke="black" ' + \
			r'(?:stroke-width="1" stroke-linejoin="round"|stroke-linejoin="round" stroke-width="1") ?/>'
	m = re.search(regex, data)
	outline = m.group(0)
	outline_dashed = outline.replace('/>', ' stroke-dasharray="1 4"/>')
	return data.replace(outline, outline_dashed)

def svg_remove_root(data):
	data = re.sub(r'<svg.*?>', '', data)
	data = data.replace('</svg>', '')
	return data

def gen_cut_guides(x_, y_):
	guides = []

	# off the E corner
	(x,y) = (x_+392, y_+170)
	guides.append((x,y,x+98,y+170))
	guides.append((x,y,x+98,y-170))
	# off the NE corner
	(x,y) = (x_+294, y_)
	guides.append((x,y,x+196,y))
	guides.append((x,y,x-98,y-170))
	# off the NW corner
	(x,y) = (x_+98, y_)
	guides.append((x,y,x+98,y-170))
	guides.append((x,y,x-196,y))
	# off the W corner
	(x,y) = (x_, y_+170)
	guides.append((x,y,x-98,y-170))
	guides.append((x,y,x-98,y+170))
	# off the SW corner
	(x,y) = (x_+98, y_+340)
	guides.append((x,y,x-196,y))
	guides.append((x,y,x+98,y+170))
	# off the SE corner
	(x,y) = (x_+294, y_+340)
	guides.append((x,y,x-98,y+170))
	guides.append((x,y,x+196,y))

	return guides

def make_page(width, height, guides, positions, tiles, fname):
	result = ''
	result += '<?xml version="1.0"?>\n'
	result += '<svg width="%d" height="%d" xmlns="http://www.w3.org/2000/svg" version="1.1">\n' % \
		(width, height)

	while len(tiles) < len(positions):
		tiles.append('tile-blank.svg')

	result += '\n<!-- cut guides -->\n'
	for g in guides:
		result += '<path d="M %d,%d L %d,%d" stroke-width="1" stroke="#000000" />\n' % (g)

	result += '\n<!-- tile bleeds -->\n'

	bleeds = []

	for (i,position) in enumerate(positions):
		(x,y) = position

		fpath = os.path.join('.', 'tiles', tiles[i])
		result += '<!-- inserting file %s -->\n' % fpath
		svg = ''
		with open(fpath) as fp:
			svg = fp.read()

		print 'opening ' + fpath

		svg = svg_shift(svg, x, y)
		bleeds.append(tile_get_bleed(svg))
		svg = svg_dot_outline(svg)
		svg = svg_remove_root(svg)

		result += svg

	result += '</svg>\n'

	# bleeds should draw BEFORE tile strokes
	result = result.replace('<!-- tile bleeds -->\n', '<!-- tile bleeds -->\n' + \
		'\n'.join(bleeds)+'\n')

	print 'writing ' + fname
	with open(fname, 'w') as fp:
		fp.write(result)

if __name__ == '__main__':
	# layouts
	(hex_width, hex_height, page_width, page_height, margin_n, margin_e, \
		tiles_per_page, positions, description, guides) = (0,0,0,0,0,0,0,[],'',[])

	# parse args
	if len(sys.argv) != 3:
		print 'usage:'
		print '    %s <manifest> <layout>\n' % sys.argv[0]
		print ''
		print 'example:'
		print '    %s 1846.manifest layout0\n' % sys.argv[0]
		print ''
		print 'layouts: '
		print '    layout0: 1.5in flat-to-flat hexes on 8.5x11'
		sys.exit(-1)

	manifest = sys.argv[1]
	layoutName = sys.argv[2]

	if not os.path.exists(manifest):
		raise Exception('manifest file \'%s\' not found' % manifest)

	if layoutName == 'layout0':
		description = '1.5in flat-to-flat hexes on 8.5x11'
		hex_width = 392
		hex_height = 340
		page_width = 2486
		page_height = 1920
		margin_n = 110
		margin_e = 67
		tiles_per_page = 28

		# tile positions
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

		# cut guides
		for i in [5, 16, 27]:
			tmp = gen_cut_guides(*positions[i])
			guides += tmp[0:3]
			guides.append(tmp[11])
		for i in [0,1,2,3,4,5]:
			tmp = gen_cut_guides(*positions[i])
			guides.append(tmp[3])
			guides.append(tmp[4])
			if i!=5:
				guides.append(tmp[2])
		for i in [0, 11, 22]:
			tmp = gen_cut_guides(*positions[i])
			guides += tmp[5:9]
		for i in [22, 23, 24, 25, 26, 27]:
			tmp = gen_cut_guides(*positions[i])
			guides.append(tmp[9])
			guides.append(tmp[10])
			if i!=27:
				guides.append(tmp[11])
		for i in [6,17]:
			tmp = gen_cut_guides(*positions[i])
			guides += tmp[6:6+2]
		for i in [10,21]:
			tmp = gen_cut_guides(*positions[i])
			guides += tmp[0:0+2]

	else:
		raise Exception('layout \'%s\' not found' % layout)

	# go!
	ET.register_namespace('', 'http://www.w3.org/2000/svg')

	pageNum = 1

	tiles = []
	with open(manifest, 'r') as fp:
		tiles = map(lambda x: x.strip(), fp.readlines())

	while tiles:
		batch = []
		while tiles:
			# blank lines mark page boundaries
			if not tiles[0] or tiles[0].isspace():
				tiles = tiles[1:]
				break

			# add to batch, break when batch is too large
			batch.append(tiles[0])
			tiles = tiles[1:]
			if len(batch) > tiles_per_page:
				break

		make_page(page_width, page_height, guides, positions, batch, 'sheet_%02d.svg' % pageNum)
		pageNum += 1

