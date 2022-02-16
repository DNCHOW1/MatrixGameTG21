import random
import boardState

class Board:
	
	def __init__(self):
		val = list(range(1, 9))
		b = []
		for i in range(4):
			num = random.randint(0, len(val) - 1)
			b.append(val[num])
			val.remove(val[num])
		b.append(9)
		for i in range(4):
			num = random.randint(0, len(val) - 1)
			b.append(val[num])
			val.remove(val[num])
		self.boardState = boardState.BoardState(b, [])
	
	def playCard(self, moveObj):
		self.boardState = self.boardState.playCard(moveObj)
	