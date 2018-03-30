#!/usr/bin/env python

import os
import sys
import shutil
import subprocess

# target paper size in inches (landscape US letter)
paper_w_in = 11.0
paper_h_in = 8.5

# target card size in inches (MTG is 2.5 x 3.5)
card_w_in = 2.5 * .95
card_h_in = 3.5 * .95
print "aiming for printed cards that are %f x %f inches" % (card_w_in, card_h_in)

# top left corner where cards start
startpos_x_in = 1
startpos_y_in = 1

# from the raw card images to the cropped card images
card_w = 665
card_h = 970
card_offs_x = 78
card_offs_y = 78

px_per_in = max(card_w / card_w_in, card_h / card_h_in)
print "calculated %d pixels/inch for the cards" % px_per_in

paper_w = paper_w_in * px_per_in
paper_h = paper_h_in * px_per_in
print "calculated %d x %d paper" % (paper_w, paper_h)

startpos_x = startpos_x_in * px_per_in
startpos_y = startpos_y_in * px_per_in
print "drawing cards starting at %d,%d" % (startpos_x, startpos_y)

files = [
	'Ui5ZN3Y.png', 'Jd9pKa8.png', 'UcpkBaX.png', 'mYSnRmN.png', 'v5SLf5U.png',
	'VtC83bu.png', '9dEOdMQ.png', 'gIZFV49.png', 'Vfk4duq.png', 'exf7fSs.png',
	'oLlBUWl.png', 'e4K8xnJ.png', '7fzBsFG.png', 'j1ZzBsL.png', '2oCZeOT.png',
	'dolrS90.png', 'TPtiT33.png', 'M9EIOoX.png', 'O6ZwShl.png', 'EgWsgTT.png',
	'eKIVuvl.png', 'z7v7gQl.png', 'DhLrQ7D.png', 'USUnkzh.png', 'zMlU9ws.png',
	'rc5Gipz.png', 'lIg0E19.png', '0E7QQ4W.png', '0sSIuF4.png', 'i82oKeh.png',
	'pbdDf2x.png', 'mT0sjWv.png', 'OkH8CHY.png', 'ybS9yhQ.png', 'YsNrL56.png',
	'uvDUzRI.png', 'N00I7a1.png', 'rPhkftC.png', 'JEHbSNH.png', 'hjVqd6e.png',
	'Xlc9eRB.png', 'wQ2Yolf.png', 'K3xi0Lj.png', 'ckR6Lwm.png', 'y1a7WFu.png',
	'YljPwlw.png', 'juycNBY.png', 'TwIivJj.png', 'PSIblK0.png', 'W4SljjG.png',
	'5BPZie6.png', 'HwLr1Lr.png', 'txnWRpW.png', 'bXlVP9Z.png', 'L92KFNh.png',
	'ntEEl1J.png', 'hPgygzB.png', 'amGKBFJ.png', 'Ci5BS4t.png', 'mudObqd.png',
	'YzHuR0d.png', 'KuwusZV.png', '71m1w3i.png', '9RwVakv.png', 'lzumrHX.png',
	'lS8kMod.png', 'F9WFzNv.png', 'TOr4YQV.png', '1IBnyun.png', 'jknaDzA.png'
]

sheet = 0

# want pixel-wide guide lines around every card
card_w += 2
card_h += 2

# calculate card positions
positions = []
positions.append([startpos_x + 0*card_w, startpos_y + 0*card_h])
positions.append([startpos_x + 1*card_w, startpos_y + 0*card_h])
positions.append([startpos_x + 2*card_w, startpos_y + 0*card_h])
positions.append([startpos_x + 0*card_w, startpos_y + 1*card_h])
positions.append([startpos_x + 1*card_w, startpos_y + 1*card_h])
positions.append([startpos_x + 2*card_w, startpos_y + 1*card_h])

def imagemagick(args):
	print 'calling:', ' '.join(args)
	subprocess.call(args)

def usletter_rulersheet(w, h):
	csname = 'ruler.png'
	px_per_in = w/11.0

	args = ['convert', '-size', '%dx%d' % (paper_w, paper_h), 'xc:white', csname]
	imagemagick(args)

	args = ['convert']
	# draw vertical lines to the right of center
	(x,y) = (w/2.0, h/2.0)
	while x < w:
		args += ['-draw', 'line %d,%d %d,%d' % (x,0, x,h)]
		x += px_per_in
	# draw vertical lines to the left of center
	(x,y) = (w/2.0, h/2.0)
	while x >= 0:
		args += ['-draw', 'line %d,%d %d,%d' % (x,0, x,h)]
		x -= px_per_in
	# draw horizontal lines above center
	(x,y) = (w/2.0, h/2.0)
	while y >= 0:
		args += ['-draw', 'line %d,%d %d,%d' % (0,y, w,y)]
		y -= px_per_in
	# draw horizontal lines below center
	(x,y) = (w/2.0, h/2.0)
	while y < h:
		args += ['-draw', 'line %d,%d %d,%d' % (0,y, w,y)]
		y += px_per_in
	#
	args += [csname, csname]
	imagemagick(args)

def blank_sheet():
	# generate test sheet
	csname = 'card_sheet_blank.png'
	args = ['convert', '-size', '%dx%d' % (paper_w, paper_h), 'xc:white', csname]
	imagemagick(args)
	for (x,y) in positions:
		# draw crop lines
		args = ['convert']
		args += ['-draw', 'line %d,%d %d,%d' % (0,y, paper_w,y)]
		args += ['-draw', 'line %d,%d %d,%d' % (x,0, x,paper_h)]
		args += ['-draw', 'line %d,%d %d,%d' % (0,y+card_h+2,paper_w,y+card_h+2)]
		args += ['-draw', 'line %d,%d %d,%d' % (x+card_w+2,0,x+card_w+2,paper_h)]
		args += [csname, csname]
		imagemagick(args)

if __name__ == '__main__':
	blank_sheet()

	# generate the real card sheets
	while files:
		group = files[0:6]

		csname = 'card_sheet_%d.png' % sheet

		# generate blank sheet
		shutil.copy('card_sheet_blank.png', csname)

		# for each card
		for (i,fname) in enumerate(group):
			(x,y) = positions[i]

			# crop to card.png
			args = ['convert', '-crop', '%dx%d+%d+%d' % (card_w, card_h, card_offs_x, card_offs_y), './cards/%s' % fname, 'card.png']
			imagemagick(args)
			# insert it
			args = ['composite', '-gravity', 'NorthWest', '-geometry', '+%d+%d' % (x+1, y+1), 'card.png', csname, csname]
			imagemagick(args)

		print ''

		files = files[6:]
		sheet += 1

