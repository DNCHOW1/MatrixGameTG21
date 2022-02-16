import copy
from enums import Card
from enums import Position
from moveObj import MoveObj
from util import log

class BoardState:
	
	def __init__(self, board, history):
		self.board = board # board is a list of 9 ints
		self.history = history # history is a list of MoveObj
	
	# returns value at the given row/col
	def at(self, row, col):
		# invalid coords
		if row < 0 or row > 2 or col < 0 or col > 2:
			return -1
		# return correct value
		return self.board[row*3 + col]
	
	# returns index of val, -1 if invalid val
	def getPos(self, val):
		for i in range(9):
			if self.board[i] == val:
				return i
		return -1
	
	def printBoard(self):
		log(str(self.board[0]) + " " + str(self.board[1]) + " " + str(self.board[2]))
		log(str(self.board[3]) + " " + str(self.board[4]) + " " + str(self.board[5]))
		log(str(self.board[6]) + " " + str(self.board[7]) + " " + str(self.board[8]))
	
	def getNull(self, pos, card):
		newHistory = copy.deepcopy(self.history)
		newBoard = copy.deepcopy(self.board)
		newHistory.append(MoveObj(pos, card, [-1]))
		return BoardState(newBoard, newHistory)
	
	def playCard(self, moveObj):
		newHistory = copy.deepcopy(self.history)
		newBoard = copy.deepcopy(self.board)
		
		if moveObj.card == Card.INVALID:
			newHistory.append(moveObj)
			return BoardState(newBoard, newHistory)
		if moveObj.card == Card.SWITCHCORNERS:
			# error checking
			if moveObj.args == None or len(moveObj.args) != 2:
				return self.getNull(moveObj.pos, Card.SWITCHCORNERS)
			f = self.getPos(moveObj.args[0])
			s = self.getPos(moveObj.args[1])
			if f == -1 or s == -1 or f == 1 or s == 1 or f == 3 or f == 4 or f == 5 or s == 3 or s == 4 or s == 5 or f == 7 or s == 7:
				return self.getNull(moveObj.pos, Card.SWITCHCORNERS)
			# successful behavior
			newBoard[f] = self.board[s]
			newBoard[s] = self.board[f]
			newHistory.append(moveObj)
			return BoardState(newBoard, newHistory)
		if moveObj.card == Card.SWITCHEDGES:
			# error checking
			if moveObj.args == None or len(moveObj.args) != 2:
				return self.getNull(moveObj.pos, Card.SWITCHEDGES)
			f = self.getPos(moveObj.args[0])
			s = self.getPos(moveObj.args[1])
			if f == -1 or s == -1 or f == 0 or s == 0 or f == 2 or f == 4 or f == 6 or s == 2 or s == 4 or s == 6 or f == 8 or s == 8:
				return self.getNull(moveObj.pos, Card.SWITCHEDGES)
			# successful behavior
			newBoard[f] = self.board[s]
			newBoard[s] = self.board[f]
			newHistory.append(moveObj)
			return BoardState(newBoard, newHistory)
		if moveObj.card == Card.SHIFTNORTH:
			# error checking
			if moveObj.args == None or len(moveObj.args) != 1:
				return self.getNull(moveObj.pos, Card.SHIFTNORTH)
			f = self.getPos(moveObj.args[0])
			if f == -1:
				return self.getNull(moveObj.pos, Card.SHIFTNORTH)
			# successful behavior
			newBoard[f] = self.board[(f + 3) % 9]
			newBoard[(f + 3) % 9] = self.board[(f + 6) % 9]
			newBoard[(f + 6) % 9] = self.board[f]
			newHistory.append(moveObj)
			return BoardState(newBoard, newHistory)
		if moveObj.card == Card.SHIFTSOUTH:
			# error checking
			if moveObj.args == None or len(moveObj.args) != 1:
				return self.getNull(moveObj.pos, Card.SHIFTSOUTH)
			f = self.getPos(moveObj.args[0])
			if f == -1:
				return self.getNull(moveObj.pos, Card.SHIFTSOUTH)
			# successful behavior
			newBoard[f] = self.board[(f - 3) % 9]
			newBoard[(f - 3) % 9] = self.board[(f - 6) % 9]
			newBoard[(f - 6) % 9] = self.board[f]
			newHistory.append(moveObj)
			return BoardState(newBoard, newHistory)
		if moveObj.card == Card.SHIFTWEST:
			# error checking
			if moveObj.args == None or len(moveObj.args) != 1:
				return self.getNull(moveObj.pos, Card.SHIFTWEST)
			f = self.getPos(moveObj.args[0])
			if f == -1:
				return self.getNull(moveObj.pos, Card.SHIFTWEST)
			# successful behavior
			base = f - f % 3
			newBoard[base] = self.board[base + 1]
			newBoard[base + 1] = self.board[base + 2]
			newBoard[base + 2] = self.board[base]
			newHistory.append(moveObj)
			return BoardState(newBoard, newHistory)
		if moveObj.card == Card.SHIFTEAST:
			# error checking
			if moveObj.args == None or len(moveObj.args) != 1:
				return self.getNull(moveObj.pos, Card.SHIFTEAST)
			f = self.getPos(moveObj.args[0])
			if f == -1:
				return self.getNull(moveObj.pos, Card.SHIFTEAST)
			# successful behavior
			base = f - f % 3
			newBoard[base] = self.board[base + 2]
			newBoard[base + 1] = self.board[base]
			newBoard[base + 2] = self.board[base + 1]
			newHistory.append(moveObj)
			return BoardState(newBoard, newHistory)
		if moveObj.card == Card.SWAPEVEN:
			# error checking
			if moveObj.args == None or len(moveObj.args) != 1:
				return self.getNull(moveObj.pos, Card.SWAPEVEN)
			f = self.getPos(moveObj.args[0])
			if f == -1 or f == 4 or moveObj.args[0] % 2 == 1:
				return self.getNull(moveObj.pos, Card.SWAPEVEN)
			# successful behavior
			newBoard[f] = self.board[4]
			newBoard[4] = self.board[f]
			newHistory.append(moveObj)
			return BoardState(newBoard, newHistory)
		if moveObj.card == Card.SWAPODD:
			# error checking
			if moveObj.args == None or len(moveObj.args) != 1:
				return self.getNull(moveObj.pos, Card.SWAPODD)
			f = self.getPos(moveObj.args[0])
			if f == -1 or f == 4 or moveObj.args[0] % 2 == 0:
				return self.getNull(moveObj.pos, Card.SWAPODD)
			# successful behavior
			newBoard[f] = self.board[4]
			newBoard[4] = self.board[f]
			newHistory.append(moveObj)
			return BoardState(newBoard, newHistory)
		if moveObj.card == Card.ROTATECLOCKWISE:
			# error checking
			if moveObj.args == None or len(moveObj.args) != 0:
				return self.getNull(moveObj.pos, Card.ROTATECLOCKWISE)
			# successful behavior
			newBoard[0] = self.board[3]
			newBoard[1] = self.board[0]
			newBoard[2] = self.board[1]
			newBoard[5] = self.board[2]
			newBoard[8] = self.board[5]
			newBoard[7] = self.board[8]
			newBoard[6] = self.board[7]
			newBoard[3] = self.board[6]
			newHistory.append(moveObj)
			return BoardState(newBoard, newHistory)
		if moveObj.card == Card.ROTATECOUNTERCLOCKWISE:
			# error checking
			if moveObj.args == None or len(moveObj.args) != 0:
				return self.getNull(moveObj.pos, Card.ROTATECOUNTERCLOCKWISE)
			# successful behavior
			newBoard[0] = self.board[1]
			newBoard[1] = self.board[2]
			newBoard[2] = self.board[5]
			newBoard[5] = self.board[8]
			newBoard[8] = self.board[7]
			newBoard[7] = self.board[6]
			newBoard[6] = self.board[3]
			newBoard[3] = self.board[0]
			newHistory.append(moveObj)
			return BoardState(newBoard, newHistory)
		
		return self.getNull(moveObj.pos, Card.INVALID)