#!/usr/bin/env python

import re
import math
import cairo
import random
from PIL import Image

DEBUG = True

margin_x = 4
margin_y = 4

hex_r = 95.0
track_width = 10
track_width_bg = 15
hex_outline_width = 5

total_rows = 3
hex_per_row = 3

save_ink = True
save_ink = False

color_default = (1, 1, 1)
#color_default = (0, 0, 0)
#color_default = (.8, .8, .8)
color_black = (0, 0, 0)
color_white = (1, 1, 1)
color_red = (1, 0, 0)
color_green = (0, 0x99/255.0, 0)
color_yellow = (1, 1, 0)
color_brown = (0xb3/255.0, 0x73/255.0, 0x0a/255.0)
color_grey = (0x99/255.0, 0x99/255.0, 0x99/255.0)


###############################################################################
# measuring, coordinates
###############################################################################

hex_w = 2.0*hex_r

hex_h = math.sqrt(3)*hex_r
hex_rr = hex_h/2

# calculate width and height to meet target ratio
dpi = 72
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

def drawCrossHatch(cr, x, y, width, height, color, spacing=4):
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

	for k in xrange(start, end, spacing):
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

def drawHex(x, y, info):
	print '-> (%d,%d)' % (x, y)

	points = [[x, y - hex_r], [x - hex_rr, y-hex_r/2], [x - hex_rr, y+hex_r/2], \
		[x, y + hex_r], [x + hex_rr, y+hex_r/2], [x + hex_rr, y-hex_r/2], \
		[x, y - hex_r]]

	# 1) guide lines
	cr.set_line_width(.5)	
	cr.set_source_rgb(0,0,0)
	for i in range(6):
		(p1,p2) = (None, None)
		(x1,y1) = points[i]
		(x2,y2) = points[i+1]
		if x1 == x2:
			p1 = [x1,0]
			p2 = [x2,height_px]
		else:
			m = 1.0*(y2-y1)/(x2-x1)
			b = -1*m*x1 + y1	
			print 'y = %f*x + %f' % (m, b)
			p1 = [0, b]
			p2 = [width_px, m*width_px + b]
		cr.move_to(*p1)
		cr.line_to(*p2)
		cr.stroke()

	# 1) fill
	cr.set_source_rgb(*color_white)
	cr.move_to(*points[0])
	for i in range(6):
		cr.line_to(*points[i+1])
	cr.fill()

	color = info['color']

	if(save_ink):
		cr.move_to(*points[0])
		for i in xrange(1,6):
			cr.line_to(*points[i])
		cr.close_path()
		cr.clip()
		drawCrossHatch(cr, x-hex_rr, y-hex_r, 2*hex_rr, 2*hex_r, color)
		cr.reset_clip()
	else:
		cr.set_source_rgb(*color)
		cr.move_to(*points[0])
		for i in range(6):
			cr.line_to(*points[i+1])
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

	for track in info['tracks']:
		track_type = ''
		(p1,p2) = (None,None)
		(arc_center, arc_radius, arc_angle1, arc_angle2) = (0,0,0,0)

		if track in ['NE-SW', 'SW-NE', 'NW-SE', 'SE-NW', 'E-W', 'W-E', \
		  'E-C', 'SE-C', 'SW-C', 'W-C', 'NW-C', 'NE-C']:
			track_type = 'straight'
			(src,dst) = track.split('-')
			p1 = lookup[src]
			p2 = lookup[dst]

		elif track in ['NE-E', 'E-NE']:
			track_type = 'arc'
			arc_center = [x+hex_rr, y-hex_r/2]
			arc_radius = hex_r/2
			arc_angle1 = math.pi/2.0
			arc_angle2 = (210/360.0)*2*math.pi
		elif track in ['NW-SW', 'SW-NW']:
			track_type = 'arc'
			arc_center = [x-2*hex_rr, y]
			arc_radius = hex_r*1.5
			arc_angle1 = (330/360.0)*2*math.pi
			arc_angle2 = (30/360.0)*2*math.pi
		
		cr.set_line_cap(cairo.LINE_CAP_BUTT)

		if track_type == 'straight':
			cr.set_line_width(track_width_bg)
			cr.set_source_rgb(1,1,1)
			cr.move_to(*p1)
			cr.line_to(*p2)
			cr.stroke()

			cr.set_line_width(track_width)
			cr.set_source_rgb(0,0,0)
			cr.move_to(*p1)
			cr.line_to(*p2)
			cr.stroke()
		elif track_type == 'arc':
			cr.set_line_width(track_width_bg)
			cr.set_source_rgb(1,1,1)
			cr.arc(arc_center[0], arc_center[1], arc_radius, arc_angle1, arc_angle2)
			cr.stroke()

			cr.set_line_width(track_width)
			cr.set_source_rgb(0,0,0)
			cr.arc(arc_center[0], arc_center[1], arc_radius, arc_angle1, arc_angle2)
			cr.stroke()

	# 3) border
#	cr.set_line_cap(cairo.LINE_CAP_ROUND)
#	cr.set_line_width(hex_outline_width)	
#	cr.set_source_rgb(0,0,0)
#	for i in range(6):
#		cr.move_to(*points[i])
#		cr.line_to(*points[i+1])
#		cr.stroke()

	if info.get('town'):
		cr.set_source_rgb(1,1,1)
		cr.move_to(x, y);
		cr.arc(x, y, hex_r/7, 0, 2*math.pi)
		cr.fill()

		cr.set_source_rgb(0,0,0)
		cr.move_to(x, y);
		cr.arc(x, y, hex_r/8, 0, 2*math.pi)
		cr.fill()

	if info.get('city1'):
		cr.set_source_rgb(0,0,0)
		cr.move_to(x, y);
		cr.arc(x, y, hex_r/3, 0, 2*math.pi)
		cr.fill()

		cr.set_source_rgb(1,1,1)
		cr.move_to(x, y);
		cr.arc(x, y, hex_r/4, 0, 2*math.pi)
		cr.fill()

#	text_color = lookup[key]['text_color']
#
#	if DEBUG:
#		write(key, text_color, x, y + hex_rr-12)
#
#	if lookup[key]['text']:
#		write(lookup[key]['text'], text_color, x, y)
#
#	if lookup[key]['subtext']:
#		write(lookup[key]['subtext'], text_color, x, y-hex_rr + 8)

###############################################################################
# main
###############################################################################

surface = cairo.ImageSurface(cairo.FORMAT_RGB24, width_px, height_px)
cr = cairo.Context(surface)

# default white background
drawRect(cr, 0, 0, width_px, height_px, color_white)
#drawCrossHatch(cr, 0, 0, width_px, height_px, color_black, 12)

# all hexes

positions = []

(x, y) = (hex_r + margin_x, hex_r + margin_y)
for ns in range(total_rows):
	for ew in range(hex_per_row):
		shift = [0, hex_r][ew % 2]
		positions.append([x + 2*ew*hex_rr, y + ns*(hex_r*2)+shift])

info = {'color':color_green, 'tracks':['E-W', 'NW-SE']}
drawHex(positions[0][0], positions[0][1], info)
info = {'color':color_green, 'tracks':['E-W', 'NW-SW']}
drawHex(positions[1][0], positions[1][1], info)
info = {'color':color_green, 'tracks':['NE-C', 'SE-C', 'W-C'], 'town':True}
drawHex(positions[2][0], positions[2][1], info)
info = {'color':color_yellow, 'tracks':['E-W'], 'city1':True}
drawHex(positions[3][0], positions[3][1], info)

print 'final image size: %dx%d (ratio:%f' % (width_px, height_px, 1.0*width_px/height_px)

surface.write_to_png("/tmp/quick.png")
