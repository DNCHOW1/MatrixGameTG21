from playerHandle import PlayerHandle
from moveObj import MoveObj
from enums import Card
from util import *
import random

class UserPlayerHandle(PlayerHandle):
	
	def takeTurn(self, order, pos, board, cards):
		# header info
		print("-------------------", pos, "-------------------")
		print("Order:", order)
		board.printBoard()
		print("Cards:", cards)
		
		# get input
		card = Card.INVALID
		while card.name == Card.INVALID.name:
			s = input("Enter valid move: ").split(" ")
			card = Card.INVALID
			for c in cards:
				if s[0].lower() == c.value:
					card = c
					break
			args = []
			for i in s[1:]:
				args.append(int(i))
		
		return MoveObj(pos, card, args)

class RandomBot(PlayerHandle):

	def takeTurn(self, order, pos, board, cards):
		# header info
		log("------------------- " + pos.name + " -------------------")
		log("RandomBot")
		log("Order: " + str(order))
		board.printBoard()
		log("Cards: " + str(cards))
		
		# get input
		card = cards[random.randint(0, len(cards)-1)]
		res = getPossibleArgs(board, card)
		args = res[random.randint(0, len(res)-1)]
		log(card.name + " : " + str(args))
		return MoveObj(pos, card, args)

class MaxBot(PlayerHandle):
	
	def takeTurn(self, order, pos, board, cards):
		# header info
		log("------------------- " + pos.name + " -------------------")
		log("MaxBot")
		log("Order: " + str(order))
		board.printBoard()
		log("Cards: " + str(cards))
		
		# get input
		bestCard = None
		bestScore = -100
		for card in cards:
			for args in getPossibleArgs(board, card):
				mo = MoveObj(pos, card, args)
				score = getScore(board.playCard(mo), pos)
				if score > bestScore:
					bestScore = score
					bestCard = mo
		log(card.name + " : " + str(args))
		return bestCard

class MaxDiffBot(PlayerHandle):

	def __init__(self, oppPos):
		self.oppPos = oppPos
	
	def takeTurn(self, order, pos, board, cards):
		# header info
		log("------------------- " + pos.name + " -------------------")
		log("MaxDiffBot")
		log("Order: " + str(order))
		board.printBoard()
		log("Cards: " + str(cards))
		
		# get input
		bestCard = None
		bestScore = -100
		for card in cards:
			for args in getPossibleArgs(board, card):
				mo = MoveObj(pos, card, args)
				score = getScore(board.playCard(mo), pos) - getScore(board.playCard(mo), self.oppPos)
				if score > bestScore:
					bestScore = score
					bestCard = mo
		log(card.name + " : " + str(args))
		return bestCard


class BacktrackingBot(PlayerHandle):
	"""
	This Backtracking bot uses a depth-limited minimax algorithm. 

	The minimax algorithm works by recursively playing the game from alternating 
	perspectives.When trying to select a move as player 0 (you), the goal is to 
	choose the highest value move. When trying to select a move as player 1 (your 
	opponent), the goal is to choose the lowest value move. 

	In other words, you're MAXing your score as player 0, and MINimizing your value 
	as player 1. 

	The recursion occurs when -- as player 0 for example -- you want to assess the 
	value of a particular move. You're not sure what the ultimate value of that 
	move is, so you RECURSE (i.e. call the recursive function) as player 1. Player 1
	has to assess the values of its moves too, so it recurses as player 0 (and on 
	and on). The madness stops when either the game is over (i.e. your hand is empty)
	or you've reached the recursion depth limit, at which point you return player
	0's score. 

	Important caveat to the above is that, in this game, you don't actually just swap
	perspectives from player 0 to player 1 since we have the balancing rule that requires
	the player with the highest score to go first. This means that it's possible for a 
	player to play twice when transitioning between rounds. See the logic in 
	setupBacktrackCompare() for more details. 

	A few ideas for improvement:
	1. The implementation is slow! This is mostly due to the fact that python is 
	   kinda sluggish, but I'm confident implementation improvements can produce 
	   a linear speedup.
	2. Implement alpha-beta pruning to increase search depth! A lot of material you'll 
	   find online is confusing. However it's pretty simple if you keep in mind the 
	   idea that the layer above you will never pursue your branch since you're 
	   returning something worse than the best your opponent above has seen (and thus can 
	   give up searching). Message me for more info.
	3. Use a different heuristic. Maybe the current state of the board shouldn't be 
	   used as the return value at the end of search. Maybe return a value of 1 for 
	   a win, a value of 0 for a loss, and a value between 0 and 1 when reaching the
	   search depth limit (as opposed to reaching the end of a game). 
	"""

	def takeTurn(self, order, pos, board, cards):
		
		# The deck always represents the sum total of your and your opponents cards.
		# deck and hand have the same structure: they're dictionaries that map cards 
		# to the number of those respective cards in the deck/hand
		deck = getCurDeck(board)
		hand = {}

		# initialize the hand dict using the cards list
		for c in cards:
			if c not in hand:
				hand[c] = 0
			hand[c] += 1

		# We'll need a reference to our position and our opponent's when simulating 
		# moves in the future 
		self.pos = pos
		if pos == Position.NORTH:
			self.opp_pos = Position.SOUTH
		elif pos == Position.SOUTH:
			self.opp_pos = Position.NORTH
		elif pos == Position.EAST:
			self.opp_pos = Position.WEST
		else:
			self.opp_pos = Position.EAST

		# This is how many moves into the future we'll search 
		searchLimit = 2

		# Need to keep track of the best we've seen so far
		bestScore = 0
		bestCard = Card.INVALID
		bestArgs = [0, 0]

		# We're going to iterate through every card in our hand and explore 
		# recursively 
		for c in hand.keys():
			if hand[c] == 0:
				continue
			
			# For these two cards, there are no arguments to iterate through 
			if c == Card.ROTATECLOCKWISE or c == Card.ROTATECOUNTERCLOCKWISE:
				newBoard = board.playCard(MoveObj(self.pos, c, []))
				
				# the deck and cards available to you need to change in response
				# to the the actions you take as you travel down the recursion tree
				deck[c] -= 1
				hand[c] -= 1
				score = self.backtrack(order, 0, searchLimit, 1, newBoard, getRemainingDeck(hand, deck), deck)
				
				# Need to restore the deck and hand after you've finished simulating
				deck[c] += 1
				hand[c] += 1
			
				# Update your selected move if you've found a new best score
				if score > bestScore:
					bestCard = c
					bestScore = score
					bestArgs = []

			# Iterate through all the potential ways to play a card
			for args in getPossibleArgs(board, c):
				newBoard = board.playCard(MoveObj(self.pos, c, args))

				deck[c] -= 1
				hand[c] -= 1
				score = self.backtrack(order, 0, searchLimit, 1, newBoard, getRemainingDeck(hand, deck), deck)
				deck[c] += 1
				hand[c] += 1

				if score > bestScore:
					bestCard = c
					bestScore = score
					bestArgs = args

		return MoveObj(self.pos, bestCard, bestArgs)

	def setupBacktrackCompare(self, order, depth, limit, pid, newBoard, hand, deck, card, bestScore):
		"""
		This function abstracts away the process of setting up and calling the function backtrack()

		The important thing to note here is that if you're at the end of the round (i.e. order == 1)
		you need to evalute who goes first the next round. If player 0's board score is higher than 
		player 1, then player 0 goes first, otherwise player 1 goes first.

		If you're not at the end of the round, you just switch perspectives from player 0 to player 1
		or vice versa.
		"""
		
		# Modify the deck and hand before recursing 
		deck[card] -= 1
		hand[card] -= 1

		# Get the board scores you'll need to check who goes first next round
		# (if order == 1)
		yourScore = getScore(newBoard, self.pos)
		oppScore = getScore(newBoard, self.opp_pos)

		score = 0
		# Rounds consist of two moves, so order is either 0 or 1 (with 1 being 
		# the end of the round)
		if order == 1:
			if yourScore >= oppScore:
				score = self.backtrack(0, depth+1, limit, 0, newBoard, hand if pid == 0 else getRemainingDeck(hand, deck), deck)
			else:
				score = self.backtrack(0, depth+1, limit, 1, newBoard, hand if pid == 1 else getRemainingDeck(hand, deck), deck)
		else:
			score = self.backtrack(1, depth+1, limit, pid^1, newBoard, getRemainingDeck(hand, deck), deck)
				
		hand[card] += 1
		deck[card] += 1

		if (pid == 0 and score > bestScore) or (pid == 1 and score < bestScore):
			# Return score since it's the new best value
			return score 

		# Return the same best score passed in as a parameter since you were unable to
		# find something better
		return bestScore

	def backtrack(self, order, depth, limit, pid, board, hand, deck):

		# This loop is just to check to see if there are any
		# nonzero card counts in your hand
		foundNonZero = False
		for c in hand.keys():
			if hand[c] != 0:
				foundNonZero = True
				break 

		# Base case: depth == limit or you don't have any more cards
		if depth >= limit or not foundNonZero:
			return getScore(board, self.pos)

		# So you want to iteratively find the best score right?
		# If you're player 1, you should start the best score really high and
		# lower if as you find better moves. Do the exact opposite if you're 
		# player 0 
		bestScore = 9999
		if pid == 0:
			bestScore = 0

		# Recursively explore every move available to you
		for c in hand.keys():
			if hand[c] == 0:
				continue 
			
			if c == Card.ROTATECLOCKWISE or c == Card.ROTATECOUNTERCLOCKWISE:
				newBoard = board.playCard(MoveObj(self.pos if pid == 0 else self.opp_pos, c, []))
				bestScore = self.setupBacktrackCompare(order, depth, limit, pid, newBoard, hand, deck, c, bestScore)
				
			for args in getPossibleArgs(board, c):
				newBoard = board.playCard(MoveObj(self.pos if pid == 0 else self.opp_pos, c, args))
				bestScore = self.setupBacktrackCompare(order, depth, limit, pid, newBoard, hand, deck, c, bestScore)

		return bestScore