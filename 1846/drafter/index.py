#!/usr/bin/env python
#
# web script to facilitate the player order randomization and private company draft

import os
import sys
import pickle
import random
import datetime

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
	def __init__(self, players, seed=None):
		# state of the draft:
		self.players = None			# (list) names of the players
		self.turn = None			# (int)  index of player whose turn it is
		self.deck = None			# (list) cards remaining in the draft
		self.hand = None			# (list) the cards that the current player can "see"
		self.owned = None			# (dict) player name -> list of cards owned 
		self.log = None				# (list) log entries
		self.rstate = None			# (obj)  random number generator state

		self.log = []
		self.log.append('initializing setup')

		if not seed:
			seed = random.randint(1,1000000)
		self.log.append('using seed: %d' % seed)
		random.seed(seed)

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

		self.rstate = random.getstate()

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
		#print 'deck now contains: ' + ','.join(self.deck)

		# add to player's hand
		self.owned[player].append(card)
		self.log.append(str(datetime.datetime.now()) + ' %s has chosen' % player)
	
		# advance to next player
		self.deal()
		self.nextPlayer()

	def deal(self):
		random.setstate(self.rstate)

		handAmt = len(self.players)+2

		if len(self.deck) <= handAmt:
			self.hand = list(self.deck)	
		else:
			random.shuffle(self.deck)
			self.hand = self.deck[0:handAmt]

		self.rstate = random.getstate()

	def isDone(self):
		for card in self.deck:
			if not card.startswith('Pass'):
				return False
		return True
			

state = None
if os.path.exists('state.dat'):
	with open('state.dat') as fp:
		state = pickle.load(fp)
else:
	state = State(['Alice', 'Bob', 'Carl', 'Daniel'])

form = cgi.FieldStorage()

# expected variables from CGI
op = None
if 'op' in form:
	op = form['op'].value
player = None
if 'player' in form:
	player = form['player'].value

if state.isDone():
	print 'draft is finished!<br>'
	for player in state.players:
		cards = filter(lambda x: not x.startswith('Pass'), state.owned[player])
		print '<b>%s</b> drafted %s<br>' % (player, ', '.join(cards))
	op = 'skip'

try:
#if True:
	if op == 'skip':
		pass
	elif op:
		if op == 'init':
			players = form['players'].value.split(',')
			seed = None
			if 'seed' in form:
				seed = int(form['seed'].value)
			print 're-initializing draft with players: %s<br>' % players
			state = State(players, seed)
		elif op == 'choose':
			card = form['card'].value
			state.choose(player, card)
			print 'you chose: %s' % card
	
	elif ('player' in form):
		player = form['player'].value
		if player == state.players[state.turn]:
			print 'it\'s your turn! choices:<br>'
			print '<form action=index.py>'
			print '<input type=hidden name=player value=%s>' % player
			print '<input type=hidden name=op value=choose>'
			for card in state.hand:
				print '<input type=radio name=card value="%s">%s</input>' % (card,card)
			print '<input type=submit value=choose>'
			print '</form>'
		else:
			print 'not your turn!<br>'
except Exception as e:
	print '<font color=red><b>ERROR:</b></font> %s' % str(e)

print '<br><br>'
print 'draft log:'
print '<hr>'
print '<br>\n'.join(state.log), '<br>'

with open('state.dat', 'w') as fp:
	pickle.dump(state, fp);

