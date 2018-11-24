#!/usr/bin/env python
#
# web script to facilitate the player order randomization and private company draft

import os
import sys

import pickle

import random

import cgi
import cgitb
cgitb.enable()

print 'Content-Type: text/html'
print

# privates elligable for removal:
cardsBlueRect = ['Meat Packing Company', 'Steamboat Company', 'Tunnel Blasting Company']
cardsOrangeDot = ['Michigan Central', 'Ohio & Indiana', 'Lake Shore Line']
# these privates are always in the game:
cardsOthers = ['Chicago and Western Indiana', 'Big 4', 'Michigan Southern', 'Mail Contract']
cardsPass = ['Pass#1', 'Pass#2', 'Pass#3', 'Pass#4', 'Pass#5']
# corporations elligable for removal:
cardsGreenDiamond = ['Chesapeake and Ohio Railroad', 'Erie Railroad', 'Pennsylvania Railroad']

assert(len(cardsBlueRect) + len(cardsOrangeDot) + len(cardsOthers) + len(cardsPass) == 15)

class State:
	def __init__(self, players):
		self.log = []

		self.log.append('initializing setup')

		# randomly order the players
		self.players = players
		random.shuffle(self.players)
		self.log.append('player order, starting with PD: ' + ', '.join(self.players))
		
		self.players = list(reversed(self.players))
		self.log.append('player order, draft: ' + ', '.join(self.players))

		# initiate removal
		cbr = list(cardsBlueRect)
		cod = list(cardsOrangeDot)
		cgd = list(cardsGreenDiamond)
		for i in range(5-len(players)):
			# randomly drop a corporation
			random.shuffle(cgd)
			self.log.append('remove corporation: ' + cgd[-1])
			cgd = cgd[0:-1]

			# randomly drop a private
			random.shuffle(cbr)
			self.log.append('remove private: ' + cbr[-1])
			cbr = cbr[0:-1]

			# randomly drop a private
			random.shuffle(cod)
			self.log.append('remove private: ' + cod[-1])
			cod = cod[0:-1]

		# deck is remaining privates + pass cards
		self.deck = cbr + cod + cardsOthers + cardsPass
		random.shuffle(self.deck)
		self.log.append('remaining cards: ' + ', '.join(self.deck))

		# what each player owns
		self.owned = {}
		for p in players:
			self.owned[p] = []

		# current player to move
		self.turn = -1
		self.nextPlayer()

		# deal cards to current player
		self.hand = []
		self.deal()

	def nextPlayer(self):
		self.turn = (self.turn + 1) % len(self.players)
		self.atPlayer = self.players[self.turn]
		self.log.append('advanced player to: ' + self.atPlayer)

	def choose(self, player, card):
		if player != self.atPlayer:
			raise Exception('player %s is choosing, but it\'s not their turn' % player)
		if not (card in self.hand):
			raise Exception('chose card "%s" but that\'s not in the current hand' % card)
		if not (card in self.deck):
			raise Exception('chose card "%s" but that\'s not in the current deck' % card)

		# remove from deck
		self.deck = filter(lambda x: x != card, self.deck)

		# add to player's hand
		self.owned[player].append(card)
	
		self.log.append('%s has made their choice' % player)

		self.nextPlayer()

	def deal(self):
		handAmt = len(players)+2

		if len(self.deck) <= handAmt:
			self.hand = list(self.deck)	
		else:
			random.shuffle(self.deck)
			self.hand = self.deck[0:handAmt]

state = None
if os.path.exists('state.dat'):
	with open('state.dat') as fp:
		state = pickle.load(fp)
else:
	state = State(['Alice', 'Bob', 'Carl', 'Daniel'])

form = cgi.FieldStorage()

op = None
if 'op' in form:
	op = form['op'].value
player = None
if 'player' in form:
	player = form['player'].value

if op:
	if op == 'init':
		players = form['players'].value.split(',')
		print 're-initializing draft with players: %s<br>\n' % players
		state = State(players)
	elif op == 'choose':
		state.choose(player, form['card'].value)

elif ('player' in form):
	player = form['player'].value
	if player == state.players[state.turn]:
		print 'it\'s your turn! choices:<br>\n'
		print '<form action=index.py>\n'
		print '<input type=hidden name=player value=%s>\n' % player
		print '<input type=hidden name=op value=choose>\n'
		for card in state.hand:
			print '<input type=radio name=card value="%s">%s</input>\n' % (card,card)
		print '<input type=submit value=choose>\n'
		print '</form>\n'
	else:
		print 'not your turn!<br>\n'

print '<b>draft log:</b><br><hr>\n'
print '<br>\n'.join(state.log)

with open('state.dat', 'w') as fp:
	pickle.dump(state, fp);

