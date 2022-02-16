import enums
import moveObj
import copy
from timeit import default_timer as timer

class Player:
	
	def __init__(self, handle, cards, pos):
		self.handle = handle
		self.cards = cards
		self.pos = pos
		self.elapsedTime = 0
	
	def notInHand(self, card):
		for c in self.cards:
			if c.name == card.name:
				return False
		return True
	
	def takeTurn(self, order, board):
		start = timer()
		resObj = self.handle.takeTurn(order, self.pos, copy.deepcopy(board), copy.deepcopy(self.cards))
		end = timer()
		self.elapsedTime += end - start
		# if invalid card, then play nothing and remove the first card from the deck
		if resObj == None or resObj.card == None:
			c = self.cards[0]
			self.cards.remove(c)
			return moveObj.MoveObj(self.pos, c, [-1])
		if self.notInHand(resObj.card):
			c = self.cards[0]
			self.cards.remove(c)
			return moveObj.MoveObj(self.pos, c, [-1])
		# if card is valid, then remove it from hand and play it
		self.cards.remove(resObj.card)
		# ensure that the return object has the appropriate position (for use in history)
		resObj.pos = self.pos
		return resObj