#!/usr/bin/env python

import os
import sys
import shutil
import subprocess

# target paper size in inches (landscape US letter)
dpi = 300
paper_w = 11*dpi
paper_h = 8.5*dpi

# target card size in inches (MTG is 2.5 x 3.5)
card_w = 2.5*dpi
card_h = 3.5*dpi

lookup = {
	'Adventurer':'ll1_01.jpg',
	'FalseRumors':'ll1_02.jpg',
	'Guardian':'ll1_03.jpg',
	'FlyingGarden':'ll1_04.jpg',
	'StoryTeller':'ll1_05.jpg',
	'Wound':'ll1_06.jpg',
	'Curse':'ll1_07.jpg',
	'SisterOfFate':'ll1_08.jpg',
	'General':'ll1_09.jpg',
	'ShadowThief':'ll1_10.jpg',
	'TheStarship':'ll1_11.jpg',
	'OldMap':'ll1_12.jpg',
	'Swordsman':'ll1_13.jpg',
	'Assault':'ll1_14.jpg',
	'SneakAttack':'ll1_15.jpg',
	'Search':'ll1_16.jpg',
	'Saint':'ll1_19.jpg',
	'Necromancer':'ll1_20.jpg',
	'Reference1':'ll1_17.jpg',
	'Reference2':'ll1_18.jpg'
}

# calculate card positions
startpos_x = 0 + (paper_w - 4*card_w)/2.0
startpos_y = 0 + (paper_h - 2*card_h)/2.0
positions = []
positions.append([startpos_x + 0*card_w, startpos_y + 0*card_h])
positions.append([startpos_x + 1*card_w, startpos_y + 0*card_h])
positions.append([startpos_x + 2*card_w, startpos_y + 0*card_h])
positions.append([startpos_x + 3*card_w, startpos_y + 0*card_h])
positions.append([startpos_x + 0*card_w, startpos_y + 1*card_h])
positions.append([startpos_x + 1*card_w, startpos_y + 1*card_h])
positions.append([startpos_x + 2*card_w, startpos_y + 1*card_h])
positions.append([startpos_x + 3*card_w, startpos_y + 1*card_h])

def imagemagick(args):
	print('calling:', ' '.join(args))
	subprocess.call(args)

def blank_sheet():
	# generate test sheet
	csname = 'card_sheet_blank.png'
	# create blank page
	args = ['convert', '-size', '%dx%d' % (paper_w, paper_h), 'xc:white', csname]
	imagemagick(args)
	# draw all the lines
	args = ['convert']
	for (x,y) in positions:
		# draw crop lines
		args += ['-draw', 'line %d,%d %d,%d' % (0,y, paper_w,y)]
		args += ['-draw', 'line %d,%d %d,%d' % (x,0, x,paper_h)]
		args += ['-draw', 'line %d,%d %d,%d' % (0,y+card_h+2,paper_w,y+card_h+2)]
		args += ['-draw', 'line %d,%d %d,%d' % (x+card_w+2,0,x+card_w+2,paper_h)]
	args += [csname, csname]
	imagemagick(args)

	cmd = ['convert', '-units', 'PixelsPerInch', csname, '-density', str(dpi), csname]
	imagemagick(cmd)

def gen_sheet(sheetpath, cards):
	global positions
		
	shutil.copy('card_sheet_blank.png', sheetpath)

	# generate the real card sheets
	for (i,card) in enumerate(cards):
		cardpath = os.path.join('./cards', card)

		# for each card
		(x,y) = positions[i]

		# resize to card.png
		args = ['convert', '-quality', '100', '-resize', '%dx%d!' % (card_w, card_h), cardpath, 'card.png']
		imagemagick(args)
		# insert it
		args = ['composite', '-gravity', 'NorthWest', '-geometry', '+%d+%d' % (x+1, y+1), 'card.png', sheetpath, sheetpath]
		imagemagick(args)

		cmd = ['convert', '-units', 'PixelsPerInch', sheetpath, '-density', str(dpi), sheetpath]
		imagemagick(cmd)

if __name__ == '__main__':
	blank_sheet()
	#sys.exit(-1)

	deck = 'starship'
	if len(sys.argv) > 1:
		deck = sys.argv[1]
	print("using deck: %s" % deck)

	if deck == 'starship':
		cards = ['SisterOfFate', 'General', 'ShadowThief', 'Swordsman',
			'TheStarship', 'OldMap', 'OldMap', 'Search']
		gen_sheet('card_sheet_1.png', map(lambda x: lookup[x], cards))

		cards = ['Search', 'Search', 'Assault', 'Assault',
			'Assault', 'SneakAttack', 'SneakAttack', 'SneakAttack']
		gen_sheet('card_sheet_2.png', map(lambda x: lookup[x], cards))
