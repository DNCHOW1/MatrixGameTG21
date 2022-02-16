from enums import Card
from moveObj import MoveObj

class PlayerHandle:

	def __init__(self, oppPos):
		self.oppPos = oppPos

	def takeTurn(self, order, pos, board, cards):
		print("ERROR: not implemented")
		return MoveObj(pos, Card.INVALID, [])
		# Nothing to do here... this class needs to be extended by the user and this function needs to be reimplemented