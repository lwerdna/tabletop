#!/usr/bin/env python

import re
import sys
import math
import cairo
import random
from PIL import Image

DEBUG = True
dpi = 300

#      /\
#     /  \
#    |    |
#    |    |
#     \  /
#      \/

hex_r = 1.25 * dpi
track_width = .15 * dpi
track_width_bg = .2 * dpi
town_radius = .150 * dpi
cost_radius = .175 * dpi
city_radius = .275 * dpi
city_line_width = .01 * dpi
cut_guide_margin = .5*dpi
font_size = 64

total_rows = 3
hex_per_row = 3

save_ink = True

default = (1, 1, 1)
#default = (0, 0, 0)
#default = (.8, .8, .8)
black = (0, 0, 0)
white = (1, 1, 1)
red = (1, 0, 0)
green = (0, 0x99/255.0, 0)
yellow = (1, 1, 0)
brown = (0xb3/255.0, 0x73/255.0, 0x0a/255.0)
grey = (0x99/255.0, 0x99/255.0, 0x99/255.0)


###############################################################################
# measuring, coordinates
###############################################################################

hex_h = 2.0*hex_r
hex_w = math.sqrt(3)*hex_r

hex_rr = hex_w/2

# calculate width and height to meet target ratio
width_in = 8.5
height_in = 11
width_px = int(width_in * dpi)
height_px = int(height_in * dpi)
print "pixel width/height = %d/%d" % (width_px, height_px)

###############################################################################
# funcs
###############################################################################

def drawRect(cr, x, y, width, height, color):
	cr.set_source_rgb(*color)
	cr.rectangle(x, y, width, height)
	cr.fill()	

def drawCrossHatch(cr, x, y, width, height, color, spacing=16):
	cr.set_source_rgb(*white)
	cr.rectangle(x, y, width, height)
	cr.fill()

	cr.save()
	cr.rectangle(x, y, width, height)
	cr.clip()
	cr.new_path()
	cr.set_source_rgb(*color)
	cr.set_line_width(2)

	start = int(x - height)
	end = int(x + width + height)

	for k in xrange(start, end, spacing):
		cr.move_to(k, y)
		cr.line_to(k + height, y+height)
		cr.move_to(k, y+height)
		cr.line_to(k+height, y)
	cr.stroke()
	cr.restore()

def drawCircle(x, y, radius, outline, fill, outline_width):
	cr.set_line_width(0)
	cr.set_source_rgb(*fill)
	cr.arc(x, y, radius, 0, 2*math.pi)
	cr.fill()

	cr.set_line_width(outline_width)
	cr.set_source_rgb(*outline)
	cr.arc(x, y, radius, 0, 2*math.pi)
	cr.stroke()

def extendLine(x1,y1,x2,y2):
	delta = .1*math.sqrt((x2-x1)**2 + (y2-y1)**2)

	# is vertical line?
	if x1==x2:
		if y1>y2:
			delta *= -1
		return (x1,y1,x2,y2+delta)

	# is horizontal line?
	if y1==y2:
		if x1>x2:
			delta *= -1
		return (x1, y1, x2+delta, y2)

	# else, follow the rise/run
	m = (1.0*y2-y1)/(x2-x1)
	# t^2 = (mx)^2 + x^2 (Pyth.) 
	# t^2 = m^2 x^2 + x^2
	# t^2 = x^2 (m^2 + 1)
	# x^2 = t^2 / (m^2 + 1)
	xdelta = math.sqrt(delta**2 / (m**2+1))

	if x2 < x1:
		xdelta *= -1

	x2 += xdelta
	y2 += m * xdelta

	return (x1,y1,x2,y2)

def hexpoints(x, y, r=hex_r):

	rr = math.sqrt(3)/2 * r
	result = []

	# vertices starting at 12 o'clock and moving clockwise
	result.append((x,		y-r))
	result.append((x+rr,	y-r/2.0))
	result.append((x+rr,	y+r/2.0))
	result.append((x,		y+r))
	result.append((x-rr,	y+r/2.0))
	result.append((x-rr,	y-r/2.0))

	# points between the vertices starting at 1 o'clock and moving clockwise
	result.append((x+hex_rr/2,	y-hex_r/2-hex_r/4))
	result.append((x+hex_rr,	y))
	result.append((x+hex_rr/2,	y+hex_r/2+hex_r/4))
	result.append((x-hex_rr/2,	y+hex_r/2+hex_r/4))
	result.append((x-hex_rr,	y))
	result.append((x-hex_rr/2,	y-hex_r/2-hex_r/4))

	# centroid of the 6 triangles, starting at NE and moving clockwise
	result.append(((x + result[0][0] + result[1][0])/3.0, (y + result[0][1] + result[1][1])/3.0))
	result.append(((x + result[1][0] + result[2][0])/3.0, (y + result[1][1] + result[2][1])/3.0))
	result.append(((x + result[2][0] + result[3][0])/3.0, (y + result[2][1] + result[3][1])/3.0))
	result.append(((x + result[3][0] + result[4][0])/3.0, (y + result[3][1] + result[4][1])/3.0))
	result.append(((x + result[4][0] + result[5][0])/3.0, (y + result[4][1] + result[5][1])/3.0))
	result.append(((x + result[5][0] + result[0][0])/3.0, (y + result[5][1] + result[0][1])/3.0))

	return result

def drawCutGuides(positions):
	for (x,y) in positions:
		points = hexpoints(x, y, hex_r)

		cr.set_line_width(1)	
		cr.set_source_rgb(0,0,0)

		for i in range(6):
			(p1,p2) = (None, None)
			(x1,y1) = points[i]

			if i<5:
				(x2,y2) = points[i+1]
			else:
				(x2,y2) = points[0]

			if x1 == x2:
				p1 = [x1,0]
				p2 = [x2,height_px]
			else:
				m = 1.0*(y2-y1)/(x2-x1)
				b = -1*m*x1 + y1	
				p1 = [0, b]
				p2 = [width_px, m*width_px + b]
			cr.move_to(*p1)
			cr.line_to(*p2)
			cr.stroke()

	cr.set_source_rgb(*white)
	cr.rectangle(0 + cut_guide_margin, 0 + cut_guide_margin, width_px - 2*cut_guide_margin, height_px - 2*cut_guide_margin)
	cr.fill()

def d2r(degrees):
	return (degrees/360.0)*2*math.pi

def write(message, color, x, y, size=0, font='Georgia', backdrop=None):
	cr.select_font_face(font)

	if not size:
		size = font_size
	cr.set_font_size(size)

	(x_bear, y_bear, width, height, x_advance, y_advance) = cr.text_extents(message)

	pos_x = x - width/2
	pos_y = y + height/2.2

	if backdrop:
		cr.set_source_rgb(*backdrop)
		cr.rectangle(pos_x, pos_y-height, width+8, height+8)
		cr.fill()

	cr.set_source_rgb(*color)
	cr.move_to(pos_x, pos_y)
	cr.show_text(message)

def drawCost(x, y, cost):
	drawCircle(x, y, cost_radius, black, white, 1)
	write("%02d" % cost, black, x, y)

# eg: (0xFF, 0, 0) -> (1.0, 0, 0)
def hexRgb(r,g,b):
	return (r/255.0, g/255.0, b/255.0)

def drawHex(pos, info):
	[x,y] = pos

	points = hexpoints(x, y)

	# 1) fill

	# white background
	cr.set_source_rgb(*white)
	cr.move_to(*points[0])
	for p in (points[1:6] + [points[0]]):
		cr.line_to(*p)
	cr.fill()

	# fill color
	color = info['color']
	if(save_ink):
		r = hex_r + track_width_bg/2.0
		rr = math.sqrt(3)/2 * r

		tmp = hexpoints(x, y, r)
		cr.move_to(*tmp[0])
		for p in (tmp[1:6] + [tmp[0]]):
			cr.line_to(*p)
		cr.close_path()
		cr.clip()

		drawCrossHatch(cr, x-rr, y-r, 2*rr, 2*r, color)
		cr.reset_clip()
	else:
		tmp = hexpoints(x, y, hex_r + track_width_bg/2.0)
		cr.set_source_rgb(*color)
		cr.move_to(*tmp[0])
		for p in (tmp[1:6] + [tmp[0]]):
			cr.line_to(*p)
		cr.fill()

	# 2) track
	p_ne = [x+hex_rr/2, y-hex_r/2 - hex_r/4]
	p_e = [x+hex_rr, y]
	p_se = [x+hex_rr/2, y+hex_r/2 + hex_r/4]
	p_sw = [x-hex_rr/2, y+hex_r/2 + hex_r/4]
	p_w = [x-hex_rr, y]
	p_nw = [x-hex_rr/2, y-hex_r/2 - hex_r/4]
	p_c = [x, y]
	lookup = {'NE':p_ne, 'E':p_e, 'SE':p_se, 'SW':p_sw, 'W':p_w, 'NW':p_nw, 'C':p_c}

	# substitute straight-across tracks for 2 center-to-edge tracks
	# example: 'NE-SW' -> ['C-NE','C-SW']
	#spans = ['NE-SW', 'SW-NE', 'NW-SE', 'SE-NW', 'E-W', 'W-E']
	#tmp = filter(lambda x: x in spans, info['tracks'])
	#info['tracks'] = filter(lambda x: x not in spans, info['tracks'])
	#for t in tmp:
	#	info['tracks'] += map(lambda x: 'C-%s'%x, t.split('-'))
	#print 'new tracks are: ' + ','.join(info['tracks'])

	# calculate all arcs and lines
	layer1 = []
	layer2 = []
	for track in info['tracks']:
		if track in ['C-E', 'C-SE', 'C-SW', 'C-W', 'C-NW', 'C-NE']:
			(p1,p2) = map(lambda k: lookup[k], track.split('-'))
			layer1.append(('line', p1, p2))
		elif track in ['NE-SW', 'SW-NE', 'NW-SE', 'SE-NW', 'E-W', 'W-E']:
			(p1,p2) = map(lambda k: lookup[k], track.split('-'))
			layer2.append(('line', p1, p2))
		elif track in ['NE-E', 'E-NE']:
			layer2.append(('arc', (x+hex_rr, y-hex_r/2), hex_r/2, d2r(180), d2r(210)))
		elif track in ['NW-SW', 'SW-NW']:
			layer2.append(('arc', (x-2*hex_rr, y), hex_r*1.5, d2r(330), d2r(30)))
		elif track in ['NW-NE', 'NE-NW']:
			layer2.append(('arc', (x, y-hex_r), hex_r/2.0, d2r(30), d2r(150)))
		elif track in ['NW-E', 'E-NW']:
			layer2.append(('arc', (x+hex_rr, y-1.5*hex_r), 1.5*hex_r, d2r(90), d2r(150)))
		else:
			raise Exception("unknown track: %s" % track)

		cr.set_line_cap(cairo.LINE_CAP_SQUARE) # adds width/2 to end
		#cr.set_line_cap(cairo.LINE_CAP_ROUND)

		#if track_type == 'straight':
		#	(x1,y1,x2,y2) = extendLine(p1[0], p1[1], p2[0], p2[1])
		#	lines.append((x1,y1,x2,y2))

		#elif track_type == 'arc':
			# extend args by going a few degrees before the start and a few degrees after
		#	bleed = (2/360.0)*2*math.pi
		#	arcs.append((arc_center, arc_radius, arc_angle1-bleed, arc_angle2+bleed))


	# draw layer 1 stuff
	# 1st pass: white track background
	# 2nd pass: black track foreground
	for pass_ in (1,2):
		if pass_ == 1:
			cr.set_line_width(track_width_bg)
			cr.set_source_rgb(1,1,1)
		else:
			cr.set_line_width(track_width)
			cr.set_source_rgb(0,0,0)

		for instr in layer1:
			if instr[0] == 'line':
				(tmp,p1,p2) = instr
				cr.move_to(p1[0],p1[1])
				cr.line_to(p2[0],p2[1])
			elif instr[0] == 'arc':
				(tmp,center, radius, angle1, angle2) = instr
				cr.arc(center[0], center[1], radius, angle1, angle2)
			cr.stroke()

	# draw layer2 stuff
	# 1st pass: white background then black foreground
	for instr in layer2:
		for bgfg in (0,1):
			if bgfg == 0:
				cr.set_line_width(track_width_bg)
				cr.set_source_rgb(1,1,1)
			else:
				cr.set_line_width(track_width)
				cr.set_source_rgb(0,0,0)

			if instr[0] == 'line':
				(tmp,p1,p2) = instr
				cr.move_to(p1[0],p1[1])
				cr.line_to(p2[0],p2[1])
			elif instr[0] == 'arc':
				(tmp,center, radius, angle1, angle2) = instr
				cr.arc(center[0], center[1], radius, angle1, angle2)
			cr.stroke()

	# towns and cities	
	cr.set_line_width(city_line_width)

	if info.get('town'):
		drawCircle(x, y, town_radius, white, black, 2)
	if info.get('city1'):
		drawCircle(x, y, city_radius, black, white, city_line_width)

	for k in info:
		m = re.match(r'city2-(\d+)', k)
		if m:
			angle = int(m.group(1))/360.0 * 2*math.pi
			print 'angle: %f' % angle
			cr.save()
			cr.translate(x, y)
			cr.rotate(angle)
			cr.rectangle(-city_radius, -city_radius, 2*city_radius, 2*city_radius)
			cr.fill()	
			drawCircle(city_radius, 0, city_radius, black, white, city_line_width)
			drawCircle(-city_radius, 0, city_radius, black, white, city_line_width)
			cr.restore()

	if info.get('city3'):
		ratio = math.sqrt(3)/2
		h = ratio*(city_radius*2)
		a = [x, y-(2/3.0)*h]
		b = [x+city_radius, y+(1/3.0)*h]
		c = [x-city_radius, y+(1/3.0)*h]
		cr.set_source_rgb(*black)
		cr.move_to(a[0]-ratio*city_radius, a[1]-.5*city_radius)
		cr.line_to(a[0]+ratio*city_radius, a[1]-.5*city_radius)
		cr.line_to(b[0]+ratio*city_radius, b[1]-.5*city_radius)
		cr.line_to(b[0], b[1]+city_radius)
		cr.line_to(c[0], c[1]+city_radius)
		cr.line_to(c[0]-ratio*city_radius, c[1]-.5*city_radius)
		cr.fill()
		for (tx,ty) in [a,b,c]:
			drawCircle(tx, ty, city_radius, black, white, city_line_width)
	if info.get('city4'):
		offs = (	(city_radius,-city_radius), \
						(city_radius,+city_radius), \
						(-city_radius,+city_radius), \
						(-city_radius,-city_radius)	)

		cr.set_source_rgb(*black)
		cr.move_to(x+1*city_radius, y-2*city_radius)
		cr.line_to(x+2*city_radius, y-1*city_radius)

		cr.line_to(x+2*city_radius, y+1*city_radius)
		cr.line_to(x+1*city_radius, y+2*city_radius)

		cr.line_to(x-1*city_radius, y+2*city_radius)
		cr.line_to(x-2*city_radius, y+1*city_radius)

		cr.line_to(x-2*city_radius, y-1*city_radius)
		cr.line_to(x-1*city_radius, y-2*city_radius)
		cr.fill()

		for i in range(4):
			drawCircle(x+offs[i][0], y+offs[i][1], city_radius, black, white, city_line_width)

	# cost
	if info.get('cost'):
		# collect regions that have track going thru
		used = []
		#print 'tracks: ' + ','.join(info['tracks'])
		for track in info['tracks']:
			used += track.split('-')
		#print 'used: ' + ','.join(used)

		spots = ['NE', 'E', 'SE', 'SW', 'W', 'NW']
		spot = filter(lambda x: x not in used, spots)
		if spot:
		#	print 'normal spot'
			spot = points[12 + spots.index(spot[0])]
		else:
		#	print 'backup spot'
			spot = [x,y-(2/3.0)*hex_r]
		drawCost(spot[0], spot[1], info['cost'])

	# id
	if info.get('id'):
		cr.save()
		cr.translate(x, y+.85*hex_r)
		cr.rotate(-math.pi/6.0)
		write(str(info['id']), black, 0, 0, font_size/2, 'Georgia', white)
		cr.restore()

###############################################################################
# main
###############################################################################

surface = cairo.ImageSurface(cairo.FORMAT_RGB24, width_px, height_px)
cr = cairo.Context(surface)

print surface.get_fallback_resolution()
#sys.exit(-1)
#drawCrossHatch(cr, 0, 0, width_px, height_px, black, 12)

# calculate hex positions
x = width_px/2.0
y = height_px/2.0
positions = []
# left column
positions.append([x-hex_w,	y-hex_h-hex_r])
positions.append([x-hex_w,	y-hex_r])
positions.append([x-hex_w,	y+hex_h-hex_r])
positions.append([x-hex_w,	y+2*hex_h-hex_r])
# middle column
positions.append([x, 		y-hex_h])
positions.append([x, 		y])
positions.append([x, 		y+hex_h])
# right column
positions.append([x+hex_w,	y-hex_h-hex_r])
positions.append([x+hex_w,	y-hex_r])
positions.append([x+hex_w,	y+hex_h-hex_r])
positions.append([x+hex_w,	y+2*hex_h-hex_r])

# manifest
tile03 = {'id':3, 'color':yellow, 'tracks':['C-NE', 'C-NW'], 'town':1, 'cost':10}
tile04 = {'id':4, 'color':yellow, 'tracks':['C-NW', 'C-SE'], 'town':1, 'cost':10}
tile05 = {'id':5, 'color':yellow, 'tracks':['C-NE', 'C-NW'], 'city1':1, 'cost':20}
tile06 = {'id':6, 'color':yellow, 'tracks':['C-NW', 'C-E'], 'city1':1, 'cost':20}
tile07 = {'id':7, 'color':yellow, 'tracks':['NE-NW']}
tile08 = {'id':8, 'color':yellow, 'tracks':['NW-E']}
tile09 = {'id':9, 'color':yellow, 'tracks':['NW-SE']}

tile14 = {'id':14, 'color':green, 'tracks':['NW-SE', 'C-E', 'C-W'], 'city2-120':1, 'cost':30}
tile15 = {'id':15, 'color':green, 'tracks':['NW-SE', 'C-NE', 'C-E'], 'city2-150':1, 'cost':30}
tile19 = {'id':19, 'color':green, 'tracks':['NW-E', 'NE-SW']}
tile20 = {'id':20, 'color':green, 'tracks':['NW-SE', 'E-W']}

tile57 = {'id':57, 'color':yellow, 'tracks':['NW-SE'], 'city1':1, 'cost':20}
tile58 = {'id':58, 'color':yellow, 'tracks':['C-NW', 'C-E'], 'town':1, 'cost':10}

tile63 = {'id':63, 'color':brown, 'tracks':['NW-SE','NE-SW','E-W'], 'city2-0':1, 'cost':40}

tile80 = {'id':80, 'color':green, 'tracks':['C-NW','C-NE','C-E']}
tile81 = {'id':81, 'color':green, 'tracks':['C-NW','C-E','C-SW']}
tile82 = {'id':82, 'color':green, 'tracks':['C-NW','C-NE','C-SE']}
tile83 = {'id':83, 'color':green, 'tracks':['C-NW','C-E','C-SW']}

tile141 = {'id':141, 'color':green, 'tracks':['C-NW','C-NE','C-SE'], 'town':1, 'cost':10}
tile142 = {'id':142, 'color':green, 'tracks':['C-NW','C-E','C-SE'], 'town':1, 'cost':10}
tile143 = {'id':143, 'color':green, 'tracks':['C-NW','C-E','C-NW'], 'town':1, 'cost':10}
tile144 = {'id':144, 'color':green, 'tracks':['C-NW','C-E','C-SE'], 'town':1, 'cost':10}

tile145 = {'id':145, 'color':brown, 'tracks':['E-W','NW-SE'], 'town':1, 'cost':20}
tile146 = {'id':146, 'color':brown, 'tracks':['C-NE','C-E','NW-SE'], 'town':1, 'cost':20}
tile147 = {'id':147, 'color':brown, 'tracks':['C-NW','C-E','NE-SW'], 'town':1, 'cost':20}

tile455 = {'id':455, 'color':grey, 'tracks':['NW-SE','NE-SW','E-W'], 'city3':1, 'cost':50}

tile544 = {'id':544, 'color':brown, 'tracks':['C-E', 'C-W', 'C-NW', 'C-SE']}
tile545 = {'id':545, 'color':brown, 'tracks':['C-NE','C-E','C-NW', 'C-SE']}
tile546 = {'id':546, 'color':brown, 'tracks':['C-NW','C-E','C-NE', 'C-SW']}

tile619 = {'id':619, 'color':green, 'tracks':['NE-SW','C-NW','C-E'], 'city2-30':1, 'cost':30}
tile716 = {'id':716, 'color':green, 'tracks':['NE-SW','NW-SE','E-W'], 'city4':1, 'cost':40}

tile717 = {'id':717, 'color':brown, 'tracks':['NE-SW','NW-SE','E-W'], 'city4':1, 'cost':50}

tile718 = {'id':718, 'color':grey, 'tracks':['NE-SW','NW-SE','E-W'], 'city4':1, 'cost':60}

yellows =	[tile03]*2 + \
			[tile04]*2 + \
			[tile05]*3 + \
			[tile06]*7 + \
			[tile07]*3 + \
			[tile08]*10 + \
			[tile09]*14 + \
			[tile57]*3 + \
			[tile58]*2

greens =	[tile14]*3 + \
			[tile15]*2 + \
			[tile19]*1 + \
			[tile20]*1 + \
			[tile80]*2 + \
			[tile81]*2 + \
			[tile82]*2 + \
			[tile83]*2 + \
			[tile141]*1 + \
			[tile142]*1 + \
			[tile143]*1 + \
			[tile144]*1 + \
			[tile619]*7 + \
			[tile716]*1

browns =	[tile63]*7 + \
			[tile145]*1 + \
			[tile146]*1 + \
			[tile147]*1 + \
			[tile544]*1 + \
			[tile545]*1 + \
			[tile546]*1 + \
			[tile717]*1

greys =		[tile455]*2 + \
			[tile718]*1

if sys.argv[1:] and sys.argv[1] == 'debug':
	yellows = []
	greens = []
	browns = []
	greys = [tile455]

if sys.argv[1:] and sys.argv[1] == 'test':
	drawRect(cr, 0, 0, width_px, height_px, white)
	positions = [positions[0]]
	drawCutGuides(positions)
	tile = {'id':619, 'color':green, 'tracks':['NE-SW','C-NW','C-E'], 'city2-180':1, 'cost':30}
	drawHex(positions[0], tile)
	path = "test.png"
	print "writing %s" % path
	surface.write_to_png(path)

else:
	pageNum = 0
	
	for colorBatch in [yellows, greens, browns, greys]:
		nBatches = (len(colorBatch)+10)/11
		for nBatch in range(nBatches):
			drawRect(cr, 0, 0, width_px, height_px, white)
			drawCutGuides(positions)
	
			# go 11 at a time
			tileBatch = colorBatch[nBatch*11:(nBatch+1)*11]
			for (i,tile) in enumerate(tileBatch):
				drawHex(positions[i], tile)
	
			# write file
			path = "tiles%02d.png" % pageNum
			print "writing %s" % path
			surface.write_to_png(path)
	
			# next
			pageNum += 1


