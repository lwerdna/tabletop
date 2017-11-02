#!/usr/bin/env python

import re
import math
import cairo
from PIL import Image

DEBUG = True

margin_x = 0
margin_y = 0

hex_r = 25.0
hex_outline_width = 1

n_hex_ew = 25
n_hex_ns = 43

save_ink = True

color_default = (1, 1, 1)
#color_default = (0, 0, 0)
#color_default = (.8, .8, .8)
color_black = (0, 0, 0)
color_white = (1, 1, 1)
color_red = (1, 0, 0)
color_green = (0, 0xcc/255.0, 0x66/255.0)
color_blue = (0x33/255.0, 0x66/255.0, 0xff/255.0)
color_yellow = (1, 1, 0)
color_magenta = (1, 0, 1)

color_city = (255, 255, 255)
#color_city = (0xf9/255.0, 0xC9/255.0, 0xC4/255.0)
color_industrial = (.3,.3,.3)
color_water = (0x0, 0xBf/255.0, 0xff)
color_plains = (0xfe/255.0, 0xfe/255.0, 0xe8/255.0)
color_forest = (0xd5/255.0, 0xf5/255.0, 0xd5/255.0)
color_mountain = (0x8c/255.0, 0x84/255.0, 0x7f/255.0)

###############################################################################
# measuring, coordinates
###############################################################################

hex_w = 2.0*hex_r

hex_h = math.sqrt(3)*hex_r
hex_rr = hex_h/2

# calculate width and height to meet target ratio
width_px = margin_x + hex_r + (n_hex_ew-1)*1.5*hex_r + hex_r + margin_x
height_px = margin_y + n_hex_ns * hex_rr + margin_y+1
[width_px, height_px] = map(int, map(math.ceil, [width_px, height_px]))
print "pixel width/height = %d/%d" % (width_px, height_px)

# eg: 'A1' -> [0,0] (map coordinates)
def key2coords(key):
	m = re.match(r'^([A-Za-z]+)(\d+)$', key)
	(let, num) = m.group(1,2)
	y = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'.index(let)
	x = int(num)-1
	return [x,y]

# eg: 'A1' -> [35,35] (cairo surface position)
def key2pos(key):
	[x,y] = key2coords(key)
	return coords2pos(x,y)

# eg: (0,0) -> [35,35] (cairo surface position)
def coords2pos(x,y):
	x = margin_x + hex_r + x*1.5*hex_r
	y = margin_y + hex_rr + y*hex_rr
	return [x,y]

# eg: (0,0) -> 'A1'
def coords2key(x,y):
	return 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'[y] + str(x+1)

###############################################################################
# global hex data
###############################################################################

lookup = {}
for x in range(n_hex_ew):
	for y in range(n_hex_ns):
		key = coords2key(x,y)
		lookup[key] = {}
		lookup[key]['visible'] = True
		lookup[key]['fill'] = color_white
		lookup[key]['stroke'] = color_black
		lookup[key]['text'] = None
		lookup[key]['subtext'] = None
		lookup[key]['text_color'] = color_black

#blanks += ['M19', 'O19', 'Q19', 'S19', 'U19', 'N18', 'P18', 'R18', 'T18', 'U17']
#for k in blanks:
#	lookup[k]['visible'] = False

# 1/6 cities
#cities = ['E1', 'L2', 'E3', 'H4', 'P4', 'D6', 'L6', 'R6', 'E9', 'I9', 'S9', \
#  'O11', 'U11', 'B12', 'I13', 'U13', 'N14', 'A15', 'I15', 'U15', 'A17', \
#  'G17', 'A19']
#names = ['Chicago', 'Indianapolis', 'South Bend', 'Fort Wayne', 'Cincinnati', \
#  'Toledo', 'Columbus', 'Ashland', 'Cleveland', 'Youngstown', 'Charleston', \
#  'Clarksburg', 'Roanoake', 'Buffalo', 'Altoona', 'Lynchburg', 'Martinsburg', \
#  'Syracuse', 'Harrisburg', 'Richmond', 'Ithaca', 'Binghampton', 'Albany']
#subtext = ['3 - 7 - 7', '1 - 2 - 4', '2 - 1 - 3', '1 - 1 - 3', '2 - 2 - 4', '2 - 1 - 2', '1 - 1 - 2', '2 - 2 - 3', '1 - 2 - 4', '2 - 1 - 2', '3 - 2 - 3', '2 - 1 - 2', '2 - 1 - 2', '2 - 3 - 5', '2 - 1 - 2', '1 - 1 - 2', '2 - 1 - 2', '2 - 1 - 3', '2 - 1 - 2', '2 - 2 - 3', '2 - 1 - 2', '2 - 1 - 2', '2 - 1 - 3']
#for i in range(len(cities)):
#	lookup[cities[i]]['text'] = names[i]
#	lookup[cities[i]]['fill'] = color_city
#	lookup[cities[i]]['subtext'] = subtext[i]
#lookup['H4']['fill'] = color_magenta


###############################################################################
# funcs
###############################################################################

def drawRect(cr, x, y, width, height, color):
	cr.set_source_rgb(*color)
	cr.rectangle(x, y, width, height)
	cr.fill()	

def drawCrossHatch(cr, x, y, width, height, color):
	cr.set_source_rgb(*color_white)
	cr.rectangle(x, y, width, height)
	cr.fill()

	cr.save()
	cr.rectangle(x, y, width, height)
	cr.clip()
	cr.new_path()
	cr.set_source_rgb(*color)
	cr.set_line_width(.5)

	start = int(x - height)
	end = int(x + width + height)

	for k in xrange(start, end, 12):
		cr.move_to(k, y)
		cr.line_to(k + height, y+height)
		cr.move_to(k, y+height)
		cr.line_to(k+height, y)
	cr.stroke()
	cr.restore()

def write(message, color, x, y, font='Georgia', size=15, backdrop=None):

	cr.select_font_face(font)
	cr.set_font_size(size)

	(x_bear, y_bear, width, height, x_advance, y_advance) = cr.text_extents(message)


	pos_x = x - width/2
	pos_y = y + height/2

	if backdrop:
		cr.set_source_rgb(*backdrop)
		cr.rectangle(pos_x-4, pos_y-height-4, width+8, height+8)
		cr.fill()

	cr.set_source_rgb(*color)
	cr.move_to(pos_x, pos_y)
	cr.show_text(message)

# eg: (0xFF, 0, 0) -> (1.0, 0, 0)
def hexRgb(r,g,b):
	return (r/255.0, g/255.0, b/255.0)

def drawHex_KEY(cr, key):
	[x,y] = key2coords(key)
	print '%s -> (%d,%d)' % (key, x, y),
	[x,y] = coords2pos(x,y)
	print '-> (%d,%d)' % (x, y)

	ratio = math.sqrt(3)/2.0

	cr.set_line_width(hex_outline_width)
	cr.set_source_rgb(*lookup[key]['stroke'])

	cr.move_to(x + hex_r, y)
	cr.line_to(x + hex_r/2.0, y - ratio*hex_r)
	cr.line_to(x - hex_r/2.0, y - ratio*hex_r)
	cr.line_to(x - hex_r, y)
	cr.line_to(x - hex_r/2.0, y + ratio*hex_r)
	cr.line_to(x + hex_r/2.0, y + ratio*hex_r)
	cr.line_to(x + hex_r, y)
	cr.stroke_preserve()

	cr.set_source_rgb(*lookup[key]['fill'])
	cr.fill()

	text_color = lookup[key]['text_color']

	if DEBUG:
		write(key, text_color, x, y + hex_rr-12)

	if lookup[key]['text']:
		write(lookup[key]['text'], text_color, x, y)

	if lookup[key]['subtext']:
		write(lookup[key]['subtext'], text_color, x, y-hex_rr + 8)

###############################################################################
# main
###############################################################################

surface = cairo.ImageSurface(cairo.FORMAT_RGB24, width_px, height_px)
cr = cairo.Context(surface)

# default white background
drawRect(cr, 0, 0, width_px, height_px, color_white)

# all hexes
for x in range(n_hex_ew):
	for y in range(n_hex_ns):
		if x%2 != y%2:
			continue
		key = coords2key(x,y)
		if lookup[key]['visible'] == False:
			continue
		drawHex_KEY(cr, key)

print 'final image size: %dx%d (ratio:%f' % (width_px, height_px, 1.0*width_px/height_px)

surface.write_to_png("/tmp/quick.png")
