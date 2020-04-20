#!/usr/bin/env python3

import re
import math
import cairo
from PIL import Image

DEBUG = False

margin_x = 4
margin_y = 4

hex_r = 32.0
hex_outline_width = 1

n_hex_ew = 25
n_hex_ns = 43

fontSize = 12

save_ink = True

default = (1, 1, 1)
black = (0, 0, 0)
white = (1, 1, 1)
yellow = (0xFC/255.0, 0xEC/255.0, 0)
purple = (0xc5/255.0, 0xbd/255.0, 0xe4/255.0)
red = (0xea/255.0, 0x1b/255.0, 0x25/255.0)
blue = (0x3e/255.0, 0x46/255.0, 0xcf/255.0)
teal = (0x98/255.0, 0xda/255.0, 0xea/255.0)

###############################################################################
# measuring, coordinates
###############################################################################

hex_w = 2.0*hex_r

hex_h = math.sqrt(3)*hex_r
hex_rr = hex_h/2

# calculate width and height to meet target ratio
width_px = margin_x + hex_r + (n_hex_ew-1)*1.5*hex_r + hex_r + margin_x
height_px = margin_y + (n_hex_ns+1) * hex_rr + margin_y+1
[width_px, height_px] = map(int, map(math.ceil, [width_px, height_px]))
print("pixel width/height = %d/%d" % (width_px, height_px))

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
		lookup[key]['fill'] = white
		lookup[key]['stroke'] = black
		lookup[key]['text'] = None
		lookup[key]['subtext'] = None
		lookup[key]['text_color'] = black

blanks = 'A1 A3 A5 A7 A9 A11 B2 B4 B6 B8 B10 C1 C3 C5 C7 C9 C11 D2 D4 D6 D8 D10 E1 E3 E5 E7 E9 F2 F4 F8 G1 G3 G5 H8 H2 H4 I1 I3 I5 J2 J4 K1 K3 K5 O1 Q1 S1 R2 S3 R4 T2 T4 U1 U3 V2 V4 W1 W3 X2 X4 Y1 Y3 Y5 Z2 Z4 Z6 a1 a3 a5 b2 b4 b6 c1 c3 c5 d2 d4 d6 e1 e3 e5 f2 f4 g1 g3 g5 h2 h4 i1 i3 i5 j2 j4 k1 k3 k5 l2 l4 m1 m3 m5 n2 n4 n6 o1 o3 o5 o7 p2 p4 p6 p8 q1 q3 q5 q7 q9 q19 q21 q11 p16 o17 q17 p18 o19 p20 q23 p24 n24 A15 A17 A19 A21 A23 A25 B18 B20 B22 B24 C19 C21 C23 C25 D20 D22 D24 E21 E23 E25 F22 F24 G1 G21 G23 G25 H24 I25 O25 Q25 T24 U25 W25 Y25 a25 c25 e25 g25 i25 k25 m25 o25 q25 V24 X24 d24 f24 h24 j24 Z24 b24 W23 N14'.split()
for k in blanks:
	lookup[k]['visible'] = False

coords = 'Q3 F6 l6 Y7 G9 l12 A13 c15 Y23 S25'.split()
names = ['Lorient', 'Cherbourg', 'Bayonne', 'La Rochelle', 'La Havre', 'Toulouse', 'Dunkerque', 'Clermont', 'Geneve', 'Basel']
for i,k in enumerate(coords):
	lookup[k]['fill'] = purple
	lookup[k]['text'] = names[i]

coords = 'S5 N6 f6 K7 S7 a7 i7 R8 I9 c9 m9 P10 X10 j10 E11 I11 S11 e11 L12 P12 b12 S13 W13 i13 H14 o15 R16 X16 Z16 n16 O17 D18 J18 d18 l18 Q19 U19 Y19 g19 k19 H20 M21 a21 e21 J22 T22 p22 e23 R24 l24 K25'.split()
names = ['St. Nazaire', 'Rennes', 'Arcachon', 'St. Lo', 'Nantes', 'Rochefort', 'Morcenx', 'Angers', 'Caen', 'Angouleme', 'Tarbes', 'Le Mans', 'poitiers', 'Montauban', 'Dieppe', 'Rouen', 'Tours', 'Perigueux', 'Mantes', 'Chartres', 'Limoges', 'Orleans', 'Chateauroux', 'Capdenac', 'Amiens', 'Narbonne', 'Laroche', 'Moulins', 'Vichy', 'Beziers', 'Troyes', 'Mons', 'Reims', 'St. Etienne', 'Nimes', 'Chaumont', 'Dijon', 'Macon', 'Valence', 'Avignon', 'Sedan', 'Nancy', 'Culot', 'Grenoble', 'Metz', 'Besancon', 'Toulon', 'St. Jean-de-Maurienne', 'Mulhouse', 'Nice', 'Wissembourg']
for i,k in enumerate(coords):
	lookup[k]['fill'] = yellow
	lookup[k]['text'] = names[i]

coords = 'M1 f8 B16 c19 M25'.split()
names = ['Brest', 'Bordeaux', 'Lille', 'Lyon', 'Strasbourg']
for i,k in enumerate(coords):
	lookup[k]['fill'] = red
	lookup[k]['text'] = names[i]

coords = 'M13 L14 M15 O15 P14 O13'.split()
for i,k in enumerate(coords):
	lookup[k]['fill'] = teal

lookup['o21']['fill'] = blue
lookup['o21']['text'] = 'Marsaille'

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
#	lookup[cities[i]]['fill'] = city
#	lookup[cities[i]]['subtext'] = subtext[i]
#lookup['H4']['fill'] = magenta


###############################################################################
# funcs
###############################################################################

def drawRect(cr, x, y, width, height, color):
	cr.set_source_rgb(*color)
	cr.rectangle(x, y, width, height)
	cr.fill()	

def drawCrossHatch(cr, x, y, width, height, color):
	cr.set_source_rgb(*white)
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

def write(message, color, x, y, font='Georgia', size=fontSize, backdrop=None):

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
	print('%s -> (%d,%d)' % (key, x, y), end='')
	[x,y] = coords2pos(x,y)
	print('-> (%d,%d)' % (x, y))

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
drawRect(cr, 0, 0, width_px, height_px, white)

# all hexes
for x in range(n_hex_ew):
	for y in range(n_hex_ns):
		if x%2 != y%2:
			continue
		key = coords2key(x,y)
		if lookup[key]['visible'] == False:
			continue
		drawHex_KEY(cr, key)

print('final image size: %dx%d (ratio:%f' % (width_px, height_px, 1.0*width_px/height_px))

surface.write_to_png("map.png")
