#!/usr/bin/env python

# try to produce 1 inch grid on 8.5x11 (US Letter)
# for:
#	printer: HPX576dw MFP
#	     os: macOS 10 HighSierra
#	  notes: choose "Scale: 100%" and 
# 

import re
import math
import cairo
import random
from PIL import Image

dpi = 72
width_in = 8.5
height_in = 11

width_px = int(dpi*width_in)
height_px = int(dpi*height_in)

surface = cairo.ImageSurface(cairo.FORMAT_RGB24, width_px, height_px)
cr = cairo.Context(surface)

# default white background
cr.set_source_rgb(1,1,1)
cr.rectangle(0, 0, width_px, height_px)
cr.fill()	

# prepare lines
cr.set_source_rgb(.5, .5, .5)
cr.set_line_width(.5)

centerX = width_px/2
centerY = height_px/2
xCollect = filter(lambda x: x>0, [centerX + dpi*x for x in xrange(-10,10,1)])
yCollect = filter(lambda x: x>0, [centerY + dpi*x for x in xrange(-10,10,1)])

# vertical lines
for x in xCollect:
	cr.new_path()
	cr.move_to(x, 0)
	cr.line_to(x, height_px)
	cr.stroke()

# horizontal lines
for y in yCollect:
	cr.new_path()
	cr.move_to(0, y)
	cr.line_to(width_px, y)
	cr.stroke()

print 'final image size: %dx%d (ratio:%f' % (width_px, height_px, 1.0*width_px/height_px)

surface.write_to_png("/tmp/quick.png")
