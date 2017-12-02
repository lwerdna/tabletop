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

def drawHex(x, y):
	print '-> (%d,%d)' % (x, y)

	points = [[x, y - hex_r], [x - hex_rr, y-hex_r/2], [x - hex_rr, y+hex_r/2], \
		[x, y + hex_r], [x + hex_rr, y+hex_r/2], [x + hex_rr, y-hex_r/2], \
		[x, y - hex_r]]

	# 1) fill
	colors = [color_green, color_brown, color_yellow]
	cr.set_source_rgb(*colors[random.randint(0,len(colors)-1)])
	cr.move_to(*points[0])
	for i in range(6):
		cr.line_to(*points[i+1])
	cr.fill()

	# 2) track
	cr.set_line_cap(cairo.LINE_CAP_BUTT)
	cr.set_line_width(track_width_bg)
	cr.set_source_rgb(1,1,1)
	cr.arc(x+hex_rr, y-hex_r/2, hex_r/2, math.pi/2.0,  (210/360.0)* 2*math.pi)
	cr.stroke()

	cr.set_line_cap(cairo.LINE_CAP_BUTT)
	cr.set_line_width(track_width_bg)
	cr.set_source_rgb(1,1,1)
	cr.arc(x+2*hex_rr, y, 1.5*hex_r, (150/360.0)*2*math.pi, (210/360.0)*2*math.pi)
	cr.stroke()

	cr.set_line_width(track_width)
	cr.set_source_rgb(0,0,0)
	cr.arc(x+hex_rr, y-hex_r/2, hex_r/2, math.pi/2.0,  (210/360.0)* 2*math.pi)
	cr.stroke()


	cr.set_source_rgb(0,0,0)
	cr.arc(x+2*hex_rr, y, 1.5*hex_r, (150/360.0)*2*math.pi, (210/360.0)*2*math.pi)
	cr.stroke()

	# 3) border
	cr.set_line_cap(cairo.LINE_CAP_ROUND)
	cr.set_line_width(hex_outline_width)	
	cr.set_source_rgb(0,0,0)
	for i in range(6):
		cr.move_to(*points[i])
		cr.line_to(*points[i+1])
		cr.stroke()


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
drawCrossHatch(cr, 0, 0, width_px, height_px, color_black)

# all hexes

(x, y) = (hex_r + margin_x, hex_r + margin_y)
for ns in range(total_rows):
	for ew in range(hex_per_row):
		shift = [0, hex_r][ew % 2]
		drawHex(x + 2*ew*hex_rr, y + ns*(hex_r*2)+shift)

print 'final image size: %dx%d (ratio:%f' % (width_px, height_px, 1.0*width_px/height_px)

surface.write_to_png("/tmp/quick.png")
